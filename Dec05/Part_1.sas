/* AoC 2023 */
/* Dec05 */

%put &=sysscp;
%if %sysfunc(substr(&sysscp., 1, 3)) = WIN %then %do;
  %let execPgmPath=%sysget(SAS_EXECFILEPATH); * Hvor ligger dette SAS-program der eksekveres lige nu? ;
  %let pdlm=\;
%end;
%if %sysfunc(substr(&sysscp., 1, 3)) = LIN %then %do;
  %let execPgmPath=&_SASPROGRAMFILE.; * Hvor ligger dette SAS-program der eksekveres lige nu? ;
  %let pdlm=/;
%end;
%put &=pdlm;

%let execPgm=%sysfunc(scan(&execPgmPath.,-1,&pdlm.));
%let execPath=%sysfunc(substr(&execPgmPath., 1, %sysfunc(length(&execPgmPath.)) - %sysfunc(length(&execPgm.))));

%put &=execPgmPath;
%put &=execPgm;
%put &=execPath;

libname dat "&execPath.data";

/* Import raw input */
filename in_file "&execPath.Input&pdlm.input.txt";
*filename in_file "&execPath.Input&pdlm.example.txt";
data WORK.input;
  length inline $ 1024;
  infile in_file;
  input;
  inline = trim(left(_INFILE_));
run;
filename in_file clear;

proc sql NOPRINT;
  select max(length(inline)) into :max_length
  from WORK.input
  ;
  select count(*) into :count_rows
  from WORK.input
  ;
quit;
%put &=max_length;
%put &=count_rows;

/* Part 1 */

data WORK.tables;
  set WORK.input;
  length table       $ 32
         map_name    $ 32
         map_from    $ 32
         map_to      $ 32
         source         8
         destination    8
         range          8
         offset         8
  ;
  retain table ''
         map_name ''
         map_from ''
         map_to ''
         ;
  if index(INLINE, ':') then do;
    map_name = scan(INLINE, 1, ': ');
    map_from = scan(map_name, 1, '-');
    map_to   = scan(map_name, 3, '-');
    table = translate(map_name, '_', '-');
    if map_from = 'seeds' then do;
       map_to = 'seed';
    end;
  end;
  else if INLINE = '' then do;
    *delete;
  end;
  else do;
    destination = input(scan(INLINE, 1, ' '), 12.);
    source      = input(scan(INLINE, 2, ' '), 12.);
    range       = input(scan(INLINE, 3, ' '), 12.);
    source_range_start      = source;
    source_range_end        = source + range - 1;
    destination_range_start = destination;
    destination_range_end   = destination + range - 1;
    offset                  = destination_range_start - source_range_start;
  end;
run;

proc sql noprint;
  select distinct map_to into :area_types separated by '¤'
  from WORK.tables
  ;
  select distinct map_name into :mappings separated by '¤'
  from WORK.tables
  where map_from ^= 'seeds'
  ;
quit;
%put &=area_types;
%put &=mappings;

data WORK.mapping_order;
  length area_type          $ 32
         area_type_backward $ 32
         area_type_forward  $ 32
         area_type_start    $ 32
         mapping            $ 64
  ;
  mappings = "&mappings.";
  mapping = scan(mappings, 1, '¤');
  area_type = scan(mapping, 3, '-');
  area_type_start = area_type;
  area_type_order = 0;
  area_type_backward = scan(mapping, 1, '-');
  output;
  count = 0;
  do while (area_type_backward ^= '' and count < 25);
    count = count + 1;
    area_type = area_type_backward;
    area_type_order = area_type_order - 1;
    idx = index(mappings, '-' || compress(area_type));
    mapping = scan(substr(mappings, 1, idx + length(compress(area_type)) + 1), -1, '¤');
    area_type_backward = scan(mapping, 1, '-');
    if idx <= 0 then do;
      area_type_backward = '';
      mapping = '';
    end;
    output;
  end;

  idx = index(mappings, compress(area_type_start) || '-');
  mapping = scan(substr(mappings, idx), 1, '¤');
  area_type = scan(mapping, 3, '-');
  area_type_backward = scan(mapping, 1, '-');
  area_type_order = 1;
  output;
  area_type_forward = scan(mapping, 3, '-');
  

  count = 0;
  do while (area_type_forward ^= '' and count < 25);
    count = count + 1;
    area_type_backward = area_type;
    area_type_order = area_type_order + 1;
    idx = index(mappings, compress(area_type_forward) || '-');
    if idx > 0 then do;
      mapping = scan(substr(mappings, idx), 1, '¤');
      area_type = scan(mapping, 3, '-');
      area_type_forward = scan(mapping, 3, '-');
    end;
    else do;
      area_type_forward = '';
      mapping = '';
    end;
    output;
  end;
run;

proc sort data=WORK.mapping_order;
  by area_type_order;
run;

proc sql;
  create table WORK.table_names as
  select distinct table,
                  map_name
  from WORK.tables
  ;
quit;

data WORK.seeds;
  set WORK.tables;
  where scan(INLINE, 1, ':') = 'seeds';
  seeds_list = trim(left(scan(INLINE, 2, ':')));
  c_seed = trim(left(scan(seeds_list, 1, ' ')));
  do idx = 2 to 1000 while (c_seed ^= '');
    seed = input(c_seed, 12.);
    output;
    c_seed = trim(left(scan(seeds_list, idx, ' ')));

  end;
run;

filename tbl_crte "&execPath.table_creator.sas";
data WORK.TABLE_CREATOR;
  set WORK.TABLE_NAMES;
  file tbl_crte;
  length putline $ 1024;
  where TABLE ^= "seeds"
  ;
  putline = 'proc sql;';
  put putline;
  putline = 'create table WORK.' || compress(TABLE) || ' as';
  put putline;
  putline = 'select MAP_NAME, SOURCE_RANGE_START, SOURCE_RANGE_END, DESTINATION_RANGE_START, DESTINATION_RANGE_END, OFFSET';
  put putline;
  putline = 'from WORK.TABLES';
  put putline;
  putline = 'where INLINE ^= "" and MAP_NAME = "' || compress(MAP_NAME) || '" and scan(INLINE, 1, " ") ^= MAP_NAME';
  put putline;
  putline = ';quit;';
  put putline;
run;
%include tbl_crte;
filename tbl_crte CLEAR;


filename joincrte "&execPath.join_creator.sas";
data WORK.JOIN_CREATOR;
  set WORK.mapping_order;
  file joincrte;
  where MAPPING ^= '';
  length putline     $ 1024
         from_table  $   32
         from_var    $   32
         ;

  retain from_table 'seeds'
         from_var   'seed'
  ;

  putline = 'proc sql;';
  put putline;

  putline = 'create table WORK.seeds_to_' || compress(area_type) || ' as';
  put putline;
  putline = 'select ';
  put putline;
  if from_var ^= 'seed' then do;
    putline = 'a.seed,';
    put putline;
  end;
  putline = ' a.' || compress(from_var) || ',';
  put putline;
  putline = 'coalesce(a.' || compress(from_var) || ' + b.offset, a.' || compress(from_var) || ') as ' || compress(area_type) || ',';
  put putline;
  putline = ' b.*';
  put putline;
  putline = 'from WORK.' || compress(from_table) || ' a';
  put putline;
  putline = 'LEFT JOIN WORK.' || compress(translate(mapping, '_', '-')) || ' b';
  put putline;
  putline = 'on a.' || compress(from_var) || ' >= b.SOURCE_RANGE_START';
  put putline;
  putline = 'and a.' || compress(from_var) || ' <= b.SOURCE_RANGE_END;';
  put putline;

  putline = 'quit;';
  put putline;
  
  output;
  from_table = 'seeds_to_' || compress(area_type);
  from_var = compress(area_type);
run;
%include joincrte;
filename joincrte CLEAR;


proc sql;
  create table WORK.part_1_answer as
  select min(location) as part_1_answer
  from WORK.SEEDS_TO_LOCATION
  ;
quit;

data WORK.PART1;
  set WORK.part_1_answer(obs=1);
  put 'Answer to part 1: ' part_1_answer;
run;

/* Result:  */
/* Evaluation:  */


/* Part 2? */


/* Result:  */
/* Evaluation:  */
