USE [Strats_Analytics]
GO

/****** Object:  Table [dbo].[Dimensions]    Script Date: 2017/11/16 19:05:57 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[Dimensions](
	[Dime_Idx] [int] NOT NULL,
	[Dime_Ori_Label] [varchar](50) NULL,
	[Dime_Std_Label] [varchar](50) NULL,
	[Rule_Idx] [int] NULL,
	[Strats_Idx] [int] NOT NULL
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

