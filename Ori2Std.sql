/****** Script for SelectTopNRows command from SSMS  ******/


  --SELECT * FROM [marketplace_lending_cracked_dev_tables].INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'
  DELETE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_Field_mappings]
  DELETE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]

  -- Matching original field names with standard filed names, which should be done manually
  Declare @OriStdMatching table (OriFieldIdx INT,  StdFieldIdx INT)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (4,4)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (3,5)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (5,6)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (6,7)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (7,8)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (8,9)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (9,10)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (10,11)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (11,12)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (12,13)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (13,14)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (14,15)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (15,16)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (16,17)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (17,18)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (18,19)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (19,20)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (20,21)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (21,22)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (22,23)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (23,24)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (24,25)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (25,26)
 
 -- Sorting the temp matching table by standard field name
 Declare @SortedOriStdMatching table (OriFieldIdx INT,  StdFieldIdx INT)
 insert INTO @SortedOriStdMatching select * FROM @OriStdMatching order by StdFieldIdx

 -- Getting the number of rows of the matching table
 Declare @myMaxOriStdRowId INT
  --set @myMaxOriStdRowId = (select count(*) from (select row_number() over(order by StdFieldIdx) as rowID, * from @OriStdMatching) as OriStdTable)
  set @myMaxOriStdRowId = (select count(*) from @SortedOriStdMatching)

  Declare @Ori_Platform_Loan_Number VARCHAR(255), @tempOriIdx int
  set @Ori_Platform_Loan_Number = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'chinatopcredit.aug2017.loantape' and ORDINAL_POSITION = 2);
  
  declare @subquery_OriField nvarchar(max)
  declare @subquery_StdField nvarchar(max)
  -- Fill in BHHJ_Field_mappings
  Declare @myCount INT = 1;
  while @myCount <= @myMaxOriStdRowId
  begin
	Declare @tempOriField VARCHAR(255)
	set @tempOriIdx = (select OriFieldIdx from (select row_number() over(order by OriFieldIdx) as rowID, * from @SortedOriStdMatching) as OriStdTable
	where rowID = @myCount)
	set @tempOriField = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'chinatopcredit.aug2017.loantape' and ORDINAL_POSITION = @tempOriIdx);
  
	Declare @tempStdField VARCHAR(255), @tempStdIdx int
	set @tempStdIdx = (select StdFieldIdx from (select row_number() over(order by OriFieldIdx) as rowID, * from @SortedOriStdMatching) as OriStdTable
	where rowID = @myCount)
	set @tempStdField = (SELECT COLUMN_NAME FROM [marketplace_lending_cracked_prod_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'BHHJ_marketplace_consumer_loan' and ORDINAL_POSITION = @tempStdIdx);

	insert into [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_Field_mappings]
	([BHHJ_Field_Number], [platform], [OriField], [StdField]) values(@myCount, 'chinatopcredit', @tempOriField, @tempStdField)

	IF (@myCount = 1)
		BEGIN
			set @subquery_OriField = '[' + @tempOriField + ']'
			set @subquery_StdField = '[' + @tempStdField + ']';
		END
	ELSE
		BEGIN
			set @subquery_OriField = @subquery_OriField + ', ' + '[' + @tempOriField + ']'
			set @subquery_StdField = @subquery_StdField + ', ' + '[' + @tempStdField + ']';
		END
	set @myCount = @myCount + 1
  end

  --print @subquery_OriField;
  --print @subquery_StdField;

--insert into [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan] (@tempStdFieldName)
--SELECT @tempOriFieldName FROM [marketplace_lending_staging_tables].[dbo].[chinatopcredit.aug2017.loantape]

declare @sql_query nvarchar(max)
set @sql_query = 'INSERT INTO [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan] '
	+ '(' + @subquery_StdField + ', [platform], [BHHJ_Loan_number]) SELECT ' + @subquery_OriField + ','
	+ '[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform],'
    + '[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[BHHJ_Loan_Number] '
	+ 'FROM [marketplace_lending_staging_tables].[dbo].[chinatopcredit.aug2017.loantape] '
	+ 'INNER JOIN [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings] '
	+ 'ON [marketplace_lending_staging_tables].[dbo].[chinatopcredit.aug2017.loantape].[' + @Ori_Platform_Loan_Number + ']'
	+ '=[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform_Loan_Number]'
--print @sql_query
exec sp_executesql @sql_query

Declare @Ori_Cur_Repay_Date VARCHAR(255)
set @Ori_Cur_Repay_Date = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'chinatopcredit.aug2017.repayment' and ORDINAL_POSITION = 4);

Declare @Ori_Unpaied_Bal VARCHAR(255)
set @Ori_Unpaied_Bal = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'chinatopcredit.aug2017.repayment' and ORDINAL_POSITION = 5);
  
-- Update original_balance according to repayment
 set @sql_query = 'DECLARE @tempLoanTable TABLE (BHHJ_Loan_Number VARCHAR(255), Platform_Loan_Number VARCHAR(255), tempDate DATE, ori_bal FLOAT) INSERT INTO @tempLoanTable SELECT [BHHJ_Loan_Number], [Platform_Loan_Number],'
 + '[' + @Ori_Cur_Repay_Date + '], [' + @Ori_Unpaied_Bal + '] FROM [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings]
INNER JOIN [marketplace_lending_staging_tables].[dbo].[chinatopcredit.aug2017.repayment] ON [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform_Loan_Number]
=[marketplace_lending_staging_tables].[dbo].[chinatopcredit.aug2017.repayment].[' + @Ori_Platform_Loan_Number + ']'
+ 'DECLARE @tempOriBalTable TABLE (BHHJ_Loan_Number VARCHAR(255), ori_bal FLOAT)
INSERT INTO @tempOriBalTable SELECT a.[BHHJ_Loan_Number], a.[ori_bal] from @tempLoanTable a
INNER JOIN (select [BHHJ_Loan_Number], min(tempDate) as MinDate from @tempLoanTable group by BHHJ_Loan_Number) b
ON a.[BHHJ_Loan_Number] = b.[BHHJ_Loan_Number] and a.[tempDate] = b.[MinDate]

UPDATE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]
SET [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[original_balance] = tempTable.[ori_bal]
From @tempOriBalTable as tempTable
WHERE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[BHHJ_Loan_Number]
=tempTable.[BHHJ_Loan_Number]'
exec sp_executesql @sql_query

/* For Creditease, need to run seperately */
-- creditease
DECLARE @Ori_Platform_Loan_Number VARCHAR(255)
SET @Ori_Platform_Loan_Number = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'creditease.oct2017.loantape' and ORDINAL_POSITION = 1);

Declare @OriStdMatching table (OriFieldIdx INT,  StdFieldIdx INT)
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (12,22) -- gender
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (36,10) -- original_balance * 10,000
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (41,11) -- loan_origination_date
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (44,7) -- term
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (45,9) -- remaining term
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (54,6) -- int_rate
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (65,12) -- remaining_balance
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (40,13) -- service fee
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (14,17) -- service fee

  -- Sorting the temp matching table by standard field name
 Declare @SortedOriStdMatching table (OriFieldIdx INT,  StdFieldIdx INT)
 INSERT INTO @SortedOriStdMatching select * FROM @OriStdMatching order by StdFieldIdx

  -- Getting the number of rows of the matching table
 Declare @myMaxOriStdRowId INT
  --set @myMaxOriStdRowId = (select count(*) from (select row_number() over(order by StdFieldIdx) as rowID, * from @OriStdMatching) as OriStdTable)
  set @myMaxOriStdRowId = (select count(*) from @SortedOriStdMatching)

 DECLARE @subquery_OriField nvarchar(max)
 DECLARE @subquery_StdField nvarchar(max)
  -- Fill in BHHJ_Field_mappings
  DECLARE @tempOriStdMatching TABLE (BHHJ_Field_Number VARCHAR(255), platform VARCHAR(255), OriField VARCHAR(255), StdField VARCHAR(255))
  DECLARE @myCount INT = 1;
  WHILE @myCount <= @myMaxOriStdRowId
  BEGIN
	DECLARE @tempOriField VARCHAR(255), @tempOriIdx INT
	SET @tempOriIdx = (SELECT OriFieldIdx FROM (SELECT row_number() over(order by OriFieldIdx) as rowID, * from @SortedOriStdMatching) as OriStdTable
	where rowID = @myCount)
	set @tempOriField = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'creditease.oct2017.loantape' and ORDINAL_POSITION = @tempOriIdx);
  
	Declare @tempStdField VARCHAR(255), @tempStdIdx int
	set @tempStdIdx = (select StdFieldIdx from (select row_number() over(order by OriFieldIdx) as rowID, * from @SortedOriStdMatching) as OriStdTable
	where rowID = @myCount)
	set @tempStdField = (SELECT COLUMN_NAME FROM [marketplace_lending_cracked_dev_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'BHHJ_marketplace_consumer_loan' and ORDINAL_POSITION = @tempStdIdx);

	insert into @tempOriStdMatching --[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_Field_mappings]
	([BHHJ_Field_Number], [platform], [OriField], [StdField]) values(@myCount, 'creditease', @tempOriField, @tempStdField)

	IF (@myCount = 1)
		BEGIN
			set @subquery_OriField = '[' + @tempOriField + ']'
			set @subquery_StdField = '[' + @tempStdField + ']';
		END
	ELSE
		BEGIN
			set @subquery_OriField = @subquery_OriField + ', ' + '[' + @tempOriField + ']'
			set @subquery_StdField = @subquery_StdField + ', ' + '[' + @tempStdField + ']';
		END
	set @myCount = @myCount + 1
  end

declare @sql_query nvarchar(max)
set @sql_query = 'INSERT INTO [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan] '
	+ '(' + @subquery_StdField + ', [platform], [BHHJ_Loan_number]) SELECT ' + @subquery_OriField + ','
	+ '[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform],'
    + '[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[BHHJ_Loan_Number] '
	+ 'FROM [marketplace_lending_staging_tables].[dbo].[creditease.oct2017.loantape] '
	+ 'INNER JOIN [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings] '
	+ 'ON [marketplace_lending_staging_tables].[dbo].[creditease.oct2017.loantape].[' + @Ori_Platform_Loan_Number + ']'
	+ '=[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform_Loan_Number]'
--print @sql_query
exec sp_executesql @sql_query

UPDATE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]
SET gender = CASE WHEN gender = '男' THEN 'M' ELSE 'F' END
WHERE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[platform] ='creditease'

UPDATE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]
SET age = term - remaining_term
WHERE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[platform] ='creditease'

UPDATE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]
SET platform_program = 'NongZuBao'
WHERE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[platform] ='creditease'

/* For zhengda, need to run seperately */
-- zhengda
DECLARE @Ori_Platform_Loan_Number VARCHAR(255)
SET @Ori_Platform_Loan_Number = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'zhengda.oct2017.loantape' and ORDINAL_POSITION = 4);

Declare @OriStdMatching table (OriFieldIdx INT,  StdFieldIdx INT)
insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (2,1) -- tape_date
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (9,4) -- platform_program
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (10,6) -- int_rate
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (11,7) -- term
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (13,9) -- remaining_term
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (14,10) -- original_balance
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (16,11) -- loan_origination_date
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (17,12) -- remaining_balance
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (18,13) -- service fee
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (23,14) -- loan_status
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (24,15) -- del_days
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (29,16) -- province
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (30,17) -- city
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (31,18) -- del_records_1y
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (35,19) -- paid_int
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (37,20) -- paid_prin
  insert into @OriStdMatching (OriFieldIdx, StdFieldIdx)
  values (38,21) -- paid_latefee

  -- Sorting the temp matching table by standard field name
 Declare @SortedOriStdMatching table (OriFieldIdx INT,  StdFieldIdx INT)
 INSERT INTO @SortedOriStdMatching select * FROM @OriStdMatching order by StdFieldIdx

  -- Getting the number of rows of the matching table
 Declare @myMaxOriStdRowId INT
  --set @myMaxOriStdRowId = (select count(*) from (select row_number() over(order by StdFieldIdx) as rowID, * from @OriStdMatching) as OriStdTable)
  set @myMaxOriStdRowId = (select count(*) from @SortedOriStdMatching)

  DECLARE @subquery_OriField nvarchar(max)
 DECLARE @subquery_StdField nvarchar(max)
  -- Fill in BHHJ_Field_mappings
  DECLARE @tempOriStdMatching TABLE (BHHJ_Field_Number VARCHAR(255), platform VARCHAR(255), OriField VARCHAR(255), StdField VARCHAR(255))
  DECLARE @myCount INT = 1;
  WHILE @myCount <= @myMaxOriStdRowId
  BEGIN
	DECLARE @tempOriField VARCHAR(255), @tempOriIdx INT
	SET @tempOriIdx = (SELECT OriFieldIdx FROM (SELECT row_number() over(order by OriFieldIdx) as rowID, * from @SortedOriStdMatching) as OriStdTable
	where rowID = @myCount)
	set @tempOriField = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'zhengda.oct2017.loantape' and ORDINAL_POSITION = @tempOriIdx);
  
	Declare @tempStdField VARCHAR(255), @tempStdIdx int
	set @tempStdIdx = (select StdFieldIdx from (select row_number() over(order by OriFieldIdx) as rowID, * from @SortedOriStdMatching) as OriStdTable
	where rowID = @myCount)
	set @tempStdField = (SELECT COLUMN_NAME FROM [marketplace_lending_cracked_dev_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'BHHJ_marketplace_consumer_loan' and ORDINAL_POSITION = @tempStdIdx);

	insert into @tempOriStdMatching --[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_Field_mappings]
	([BHHJ_Field_Number], [platform], [OriField], [StdField]) values(@myCount, 'zhengda', @tempOriField, @tempStdField)

	IF (@myCount = 1)
		BEGIN
			set @subquery_OriField = '[' + @tempOriField + ']'
			set @subquery_StdField = '[' + @tempStdField + ']';
		END
	ELSE
		BEGIN
			set @subquery_OriField = @subquery_OriField + ', ' + '[' + @tempOriField + ']'
			set @subquery_StdField = @subquery_StdField + ', ' + '[' + @tempStdField + ']';
		END
	set @myCount = @myCount + 1
  end

  declare @sql_query nvarchar(max)
set @sql_query = 'INSERT INTO [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan] '
	+ '(' + @subquery_StdField + ', [platform], [BHHJ_Loan_number]) SELECT ' + @subquery_OriField + ','
	+ '[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform],'
    + '[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[BHHJ_Loan_Number] '
	+ 'FROM [marketplace_lending_staging_tables].[dbo].[zhengda.oct2017.loantape] '
	+ 'INNER JOIN [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings] '
	+ 'ON [marketplace_lending_staging_tables].[dbo].[zhengda.oct2017.loantape].[' + @Ori_Platform_Loan_Number + ']'
	+ '=[marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform_Loan_Number]'
--print @sql_query
exec sp_executesql @sql_query

Declare @Ori_Cur_Repay_Date VARCHAR(255)
set @Ori_Cur_Repay_Date = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'zhengda.oct2017.repayment' and ORDINAL_POSITION = 4);

Declare @Ori_Unpaied_Bal VARCHAR(255)
set @Ori_Unpaied_Bal = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'zhengda.oct2017.repayment' and ORDINAL_POSITION = 10);
  
  DECLARE @Ori_Repayment_Loan_Number VARCHAR(255)
SET @Ori_Repayment_Loan_Number = (SELECT COLUMN_NAME FROM [marketplace_lending_staging_tables].INFORMATION_SCHEMA.COLUMNS where table_name = 'zhengda.oct2017.repayment' and ORDINAL_POSITION = 1);

UPDATE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]
SET age = term - remaining_term
WHERE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[platform] ='zhengda'

-- Update original_balance according to repayment
 set @sql_query = 'DECLARE @tempLoanTable TABLE (BHHJ_Loan_Number VARCHAR(255), Platform_Loan_Number VARCHAR(255), tempDate DATE, ori_bal FLOAT) INSERT INTO @tempLoanTable SELECT [BHHJ_Loan_Number], [Platform_Loan_Number],'
 + '[' + @Ori_Cur_Repay_Date + '], [' + @Ori_Unpaied_Bal + '] FROM [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings]
INNER JOIN [marketplace_lending_staging_tables].[dbo].[zhengda.oct2017.repayment] ON [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_loan_mappings].[Platform_Loan_Number]
=[marketplace_lending_staging_tables].[dbo].[zhengda.oct2017.repayment].[' + @Ori_Repayment_Loan_Number + ']'
+ 'DECLARE @tempOriBalTable TABLE (BHHJ_Loan_Number VARCHAR(255), ori_bal FLOAT)
INSERT INTO @tempOriBalTable SELECT a.[BHHJ_Loan_Number], a.[ori_bal] from @tempLoanTable a
INNER JOIN (select [BHHJ_Loan_Number], min(tempDate) as MinDate from @tempLoanTable group by BHHJ_Loan_Number) b
ON a.[BHHJ_Loan_Number] = b.[BHHJ_Loan_Number] and a.[tempDate] = b.[MinDate]

UPDATE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan]
SET [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[original_balance] = tempTable.[ori_bal]
From @tempOriBalTable as tempTable
WHERE [marketplace_lending_cracked_dev_tables].[dbo].[BHHJ_marketplace_consumer_loan].[BHHJ_Loan_Number]
=tempTable.[BHHJ_Loan_Number]'
exec sp_executesql @sql_query