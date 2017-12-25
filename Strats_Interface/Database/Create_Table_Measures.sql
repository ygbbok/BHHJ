USE [Strats_Analytics]
GO

/****** Object:  Table [dbo].[Measures]    Script Date: 2017/11/16 19:06:19 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

SET ANSI_PADDING ON
GO

CREATE TABLE [dbo].[Measures](
	[Meas_Idx] [int] NULL,
	[Meas_Ori_Label] [varchar](50) NULL,
	[Meas_Std_Label] [varchar](50) NULL,
	[Calc_Method_Idx] [int] NULL,
	[Strats_Idx] [int] NULL,
	[calc_helper] [varchar](50) NULL,
	[format] [varchar](50) NULL
) ON [PRIMARY]

GO

SET ANSI_PADDING OFF
GO

