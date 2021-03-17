1. 支持XIP时，ivt的偏移为0x1000否则在0x400，app的偏移固定为0x2000

2. HAB的API地址
	#define HAB_RVT_RT1050_60_BASE              0x00200300    128KB ROMCP
	
3. FCB在IVT的前面，设置一些SPIFlash的信息
	flexspi_nor_config_t
	
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
	
7. 实际的boot mode 以及 boot cfg可以通过 SRC_SBMR1 来查看	encryption.c 
	return (SRC->SBMR1 & BOOT_CFG_ENCRYPTED_XIP_ENABLED_MASK) != 0;

8. bee相关
	reconfigure_bee 函数  bl2_core.c 
	bee分为region0和1，加密模式为 AES_CTR  AES_ECB
	加密采用AES_CTR模式，需要一个128bits的conuter，也就是nonce
	bee的key可以有4种方式：bee_key_sel_t
		BEEKEYSEL_BEEREGISTER = 0,  ///< BEE key from BEE configuration register (BEE_AES_KEY0_W0-3)
		BEEKEYSEL_GP4 = 1,          ///< BEE key from GP4[127:0]
		BEEKEYSEL_OTPMK = 2,        ///< BEE key from OTPMK[255:128]
		BEEKEYSEL_SW_GP2 = 3        ///< BEE key from SW_GP2[127:0]

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
		CTR模式两次加密就是解密
		region0的范围是固定的，region1的范围是动态的

	

bee分为两区域，fac一共三个，是具体的加密区域
	两个bee共用三个fac
	
	
	
需要学习的文件
arm_utilities.c 
encryption.c 
	
	
	
	
	
	
	
	
	
	
	
	