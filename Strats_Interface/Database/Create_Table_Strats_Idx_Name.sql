USE [Strats_Analytics]
GO

/****** Object:  Table [dbo].[Strats_Idx_Name]    Script Date: 2017/11/16 19:07:04 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[Strats_Idx_Name](
	[Strats_Idx] [int] NOT NULL,
	[Strats_Name] [varchar](50) NULL,
	[RT_Dir] [varchar](max) NULL,
	[Sort_by] [int] NULL,
	[Display_Top_N] [int] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

