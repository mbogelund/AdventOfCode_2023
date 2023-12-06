/* AoC 2023 */
/* Dec06 */

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

data WORK.RAW_RACE_TIMES;
  set WORK.INPUT;
  length datatype $  32
         cvalues  $ 256
  ;
  datatype = trim(left(scan(INLINE, 1, ':')));
  cvalues = trim(left(scan(INLINE, 2, ':')));
  keep datatype cvalues;
run;
proc transpose data=WORK.RAW_RACE_TIMES out=WORK.T_RACE_TIMES;
  id datatype;
  var cvalues;
run;
data WORK.RACE_TIMES;
  set WORK.T_RACE_TIMES;
  length ctime           $ 16
         cdistance       $ 16
         time_ms            8
         distance_record    8
  ;
  ctime = scan(time, 1, ' ');
  cdistance = scan(distance, 1, ' ');
  do idx = 2 to 25 while(ctime ^='');
    time_ms = input(ctime, 12.);
    distance_mm = input(cdistance, 12.);
    output;
    ctime = scan(time, idx, ' ');
    cdistance = scan(distance, idx, ' ');
  end;
run;

data WORK.RACE_CALCULATIONS WORK.PART1;
  set WORK.RACE_TIMES end=last;
  retain product 1;

  wins1 = (-1 * TIME_MS + sqrt(TIME_MS**2 - 4 * DISTANCE_MM)) / (2 * (-1));
  wins2 = (-1 * TIME_MS - sqrt(TIME_MS**2 - 4 * DISTANCE_MM)) / (2 * (-1));

  
  wins_min = min(wins1, wins2);
  wins_max = max(wins1, wins2);

  /* We have to win, tie doesnt work */
  if floor(wins_min) = ceil(wins_min) then do;
    wins_min = wins_min + 1;
  end;
  else do;
    wins_min = ceil(wins_min);
  end;
  
  if floor(wins_max) = ceil(wins_max) then do;
    wins_max = wins_max - 1;
  end;
  else do;
    wins_max = floor(wins_max);
  end;
 
  wins = wins_max - wins_min + 1;

  product = product * wins;
  output WORK.RACE_CALCULATIONS;
  if last then do;
    put 'Answer to part 1: ' product;
    output WORK.PART1;
  end;
run;



/* Result: 114400 */
/* Evaluation: Correct! */


/* Part 2? */

data WORK.RACE_TIMES2;
  set WORK.T_RACE_TIMES;
  length ctime           $ 16
         cdistance       $ 16
         time_ms            8
         distance_record    8
  ;
  ctime = compress(time);
  cdistance = compress(distance);

  time_ms = input(ctime, 16.);
  distance_mm = input(cdistance, 16.);
run;

data WORK.RACE_CALCULATIONS2 WORK.PART2;
  set WORK.RACE_TIMES2 end=last;
  retain product 1;

  wins1 = (-1 * TIME_MS + sqrt(TIME_MS**2 - 4 * DISTANCE_MM)) / (2 * (-1));
  wins2 = (-1 * TIME_MS - sqrt(TIME_MS**2 - 4 * DISTANCE_MM)) / (2 * (-1));

  
  wins_min = min(wins1, wins2);
  wins_max = max(wins1, wins2);

  /* We have to win, tie doesnt work */
  if floor(wins_min) = ceil(wins_min) then do;
    wins_min = wins_min + 1;
  end;
  else do;
    wins_min = ceil(wins_min);
  end;
  
  if floor(wins_max) = ceil(wins_max) then do;
    wins_max = wins_max - 1;
  end;
  else do;
    wins_max = floor(wins_max);
  end;
 
  wins = wins_max - wins_min + 1;

  product = product * wins;
  output WORK.RACE_CALCULATIONS2;
  if last then do;
    put 'Answer to part 2: ' product;
    output WORK.PART2;
  end;
run;



/* Result: 35925555 */
/* Evaluation: too high */

/* Result: 21039729 */
/* Evaluation: Correct! */
