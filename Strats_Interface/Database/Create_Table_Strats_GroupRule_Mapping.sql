USE [Strats_Analytics]
GO

/****** Object:  Table [dbo].[Strats_GroupRule_Mapping]    Script Date: 2017/11/16 19:06:45 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Strats_GroupRule_Mapping](
	[Rule_Name] [nvarchar](255) NULL,
	[Lower_Bound] [float] NULL,
	[Upper_Bound] [float] NULL,
	[Label] [nvarchar](255) NULL,
	[Rule_Idx] [int] NULL
) ON [PRIMARY]

GO

