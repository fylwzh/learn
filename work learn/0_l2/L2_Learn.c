术语总结
	HAB: High Assurance Boot 
	SNVS: Secure Non-Volatile Storage 
	DCP: Data co-processor
	TRNG: True Random Number Generator
	OCOTP_CTRL: On-chip One-Time Programmable Element Controller 
	CSU: Central Security Unit 
	SJC: System JTAG Controller 
	BEE: Bus Encryption Engine 

1. 支持XIP时，ivt的偏移为0x1000否则在0x400，app的偏移固定为0x2000

2. HAB的API地址
	#define HAB_RVT_RT1050_60_BASE              0x00200300    128KB ROMCP
	
	个人理解：
		HAB是NXP固化在BootRom中的代码，对外提供API的接口，
		这些API可以完成对外bootable image一些验证工作，
		比如使用CSF区域的一些签名对代码进行验证等。
	
3. FCB在IVT的前面，设置一些SPIFlash的信息
	const flexspi_nor_config_t qspiflash_config
	
4. L2将flash分成三个区域  bl2_partition_info_t
	BL2PT_BOOTLOADER 0区域：
		pi.start = BL2_FLASH_BASE_ADDRESS;   0x60000000U
        pi.size = BL2_L2_PARTITION_SIZE;		0x20000U   128KB
        pi.image_offset = (uint32_t)m_boot_hdr_ivt_start - BL2_FLASH_BASE_ADDRESS;  0x60001000 - 0x60000000U
		
	BL2PT_PRIMARY  1区域：
		pi.start = BL2_PRIMARY_PARTITION_START;		0x60000000U + 0x20000U
        pi.size = BL2_PRISEC_PARTITION_SIZE;	0x20000U   128KB
        pi.image_offset = BL2_IMAGE_OFFSET;		0x00
		
	BL2PT_SECONDARY  2区域
		pi.start = BL2_SECONDARY_PARTITION_START;	0x60000000U + 0x20000U + 0x20000U
		pi.size = BL2_PRISEC_PARTITION_SIZE;	0x20000U   128KB
		pi.image_offset = BL2_IMAGE_OFFSET;		0x00

5. 每个区域有对应的nonce信息  bl2_nonce_info_t， 分区1和2的nonce信息存储在分区0的后8Kb空间
	个人：这个nonce的值用来bee加密，并且这个值会更改

	BL2PT_BOOTLOADER 0区域：
		pni.start = 0U;
        pni.size  = 0U;
	BL2PT_PRIMARY  1区域：
		pni.start = BL2_PRIMARY_NONCE_ADDRESS;	(((0x60000000U)) + ((0x20000U)) - (2 * ((0x1000U))))
        pni.size  = BL2_NONCE_STORAGE_SIZE;		(0x1000U)  // 4KB
	BL2PT_SECONDARY  2区域
		pni.start = BL2_SECONDARY_NONCE_ADDRESS;	(((0x60000000U)) + ((0x20000U)) - ((0x1000U)))
        pni.size  = BL2_NONCE_STORAGE_SIZE;		(0x1000U)  // 4KB
	
6. HAB用的API   typedef struct hab_rvt hab_rvt_t;   hab.h 
	HAB_RVT_PTR->entry();   初始花HAB库
	HAB_RVT_PTR->check_target(type, start, bytes);  

	软件签名过程：计算软件的hash值，然后使用私钥对哈希值进行加密，加密后生成签名，解密时比较hash值。
	
7. 关于DCP
	DCP是NXP的加解密加速器，可以用硬件计算常用的加解密算法
	AES加解密的密钥（Key+IV=32B）可以设置，通过IOMUXC_GPR->GPR10;  IOMUXC_GPR->GPR3;设置
		typedef enum _dcp_key_slot
		{
			kDCP_KeySlot0     = 0U, /*!< DCP key slot 0. */
			kDCP_KeySlot1     = 1U, /*!< DCP key slot 1. */
			kDCP_KeySlot2     = 2U, /*!< DCP key slot 2.*/
			kDCP_KeySlot3     = 3U, /*!< DCP key slot 3. */
			kDCP_OtpKey       = 4U, /*!< DCP OTP key. */
			kDCP_OtpUniqueKey = 5U, /*!< DCP unique OTP key. */
			kDCP_PayloadKey   = 6U, /*!< DCP payload key. */
		} dcp_key_slot_t;
	
		IOMUXC_GPR->GPR10;  IOMUXC_GPR->GPR3;代码如下：
			switch (key_sel)
			{
			case BEEKEYSEL_OTPMK:
				/* Select key from Key MUX (SNVS/OTPMK). */
				gpr10 &= ~IOMUXC_GPR_GPR10_DCPKEY_OCOTP_OR_KEYMUX_MASK;
				/* Select [255:128] from snvs/ocotp key as dcp key */
				gpr3 |= IOMUXC_GPR_GPR3_DCP_KEY_SEL(1);

				handle->keySlot = kDCP_OtpKey;
				break;
			case BEEKEYSEL_SW_GP2:
				/* Select key from OCOTP (SW_GP2) */
				gpr10 |= IOMUXC_GPR_GPR10_DCPKEY_OCOTP_OR_KEYMUX_MASK;

				handle->keySlot = kDCP_OtpKey;
				break;
			default:
				return BL2STS_UNSUPPORTED_BEE_KEYSEL;
			}

8. bee相关
	reconfigure_bee 函数  bl2_core.c 
	bee分为region0和1，加密模式为 AES_CTR  AES_ECB
	加密采用AES_CTR模式，需要一个128bits的conuter，也就是nonce
	BEE使用的密钥可以通过efuse的设置来获取  BEE_KEY1_SEL BEE_KEY0_SEL
	bee的key可以有4种方式：bee_key_sel_t
		BEEKEYSEL_BEEREGISTER = 0,  ///< BEE key from BEE configuration register (BEE_AES_KEY0_W0-3)
		BEEKEYSEL_GP4 = 1,          ///< BEE key from GP4[127:0]
		BEEKEYSEL_OTPMK = 2,        ///< BEE key from OTPMK[255:128]
		BEEKEYSEL_SW_GP2 = 3        ///< BEE key from SW_GP2[127:0]
		
	个人：
		BEE有两个配置区域，region0和region1，他们的BEE配置信息存放在prdb中，
		可以指定4个加密区域，这些区域被称作FAC0～3
		在使用AES-CRT时，需要指定counter值，这个值是由 NOUNCE和data addr经过特定算法生成
		在使用时，将BEE的加密区域分为静态区域和动态区域：
			静态区域的配置信息在PRDB0中，他们对应的加密区域为FAC0和可选的FAC1，其中L2的代码就是在静态区域中
			静态加密区域的任何数据需要变化，他们的NOUNCE必须改变。
			动态区域的BEE配置信息是动态配置的，所以配置BEE的相关函数不能在XIP-Flash中，他们对应的加密区域为FAC2和FAC3
			其中静态区域的配置信息，即PRDB0是bootRom生成的，在动态配置BEE时，需要先让bootRom对BEE进行配置
			其实动态配置BEE就是配置BEE的NOUNCE，BEE的CTR解密需要NOUNCE和密钥。
			BEE的动态和静态加密区域FAC，不能交替出现
	
	

9. PRDB：Protection Region Descriptor Block structure
	
	/* EKIB0 offset in FlexSPI NOR flash. */
	#define FLEXSPINOR_EKIB0_OFFSET (0x400U)
	/* EPRDB0 offset in FlexSPI NOR flash. */
	#define FLEXSPINOR_EPRDB0_OFFSET (0x480U)
	/* EKIB0 offset in FlexSPI NOR flash. */
	#define FLEXSPINOR_EKIB1_OFFSET (0x800U)
	/* EPRDB0 offset in FlexSPI NOR flash. */
	#define FLEXSPINOR_EPRDB1_OFFSET (0x880U)
	
	个人：
		CTR模式两次加密就是解密,在CTR模式下，加密的是counter，使用加密的counter与plaintext异或
		region0的范围是固定的，region1的范围是动态的
		PRDB，在加密XIP时使用，在程序烧写时由flashloader创建

10. efuse boot相关
	0x450[7:0](BOOT_CFG1)  的bit1  表示是否使能EncryptedXIP
	0x460[15:8] BEE_KEY1_SEL BEE_KEY0_SEL  
		0 - From register
		1 - Reserved
		2 - From OTPMK [255:128]
		3 - FROM SW-GP2
		
	实际的boot mode 以及 boot cfg可以通过 SRC_SBMR1 来查看	encryption.c 
	return (SRC->SBMR1 & BOOT_CFG_ENCRYPTED_XIP_ENABLED_MASK) != 0;

11. boot相关
	00 Boot From Fuses   	忽略pin上的配置
		
	01 Serial Downloader	
	10 Internal Boot
	11 Reserved
	SRC Boot Mode Register (SRC_SBMR2)，从这个寄存器可以读取boot模式

bee分为两区域，fac一共三个，是具体的加密区域
	两个bee共用三个fac
	

Second stage bootloader 1.1.0.
Bootloader API version: 1.1.0.
Copyright 2020 Honeywell International Inc.
Starting the Primary image.

***************** RT App Kicker ****************
************ Version 1.9.2.0 ***************
**Build time 10:06:48 Aug 19 2020**
**SRC:0x1**
**SNVS GPR:0x0**
************************************************

Config BEE
BEE_KEY1 from OTPMK[256:128]
Config BEE
BEE_KEY1 from OTPMK[256:128]
Prepare OTA backup zone

*****secure read OTA version*****

Ready jump to the application
APP:0x800129d1
STACK:0x20020000
Authenticate Pass---



initialize by copy {
  readwrite,
  /* Place in RAM BEE related functions */
  object bl2_bee.o,
  object fsl_bee.o,  //bee相关的代码都被存放在ram中，因为配置Bee时需要关闭bee功能
  section .textrw
};

	
	
需要学习的文件
arm_utilities.c 
encryption.c 
	
	
	
	
	
	
	
	
	
	
	
	