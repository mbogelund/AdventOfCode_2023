/* AoC 2023 */
/* Dec04 */

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

/* Part 1 */
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

data _NULL_;
  set WORK.input(obs=1);
  count_winning_numbers = 0;
  count_own_numbers = 0;
  winning_numbers = scan(inline, 2, ':|');
  own_numbers = scan(inline, 2, '|');

  put winning_numbers=;
  put own_numbers=;
  if _N_ = 1 then do;
    done = 0;
    do i = 1 to 30 while (not done);
      if scan(winning_numbers, i, ' ') ^= '' then do;
        count_winning_numbers = i;
      end;
      else do;
        done = 1;
      end;
    end;
    call symput("count_winning_numbers", compress(put(count_winning_numbers, 16.)));

    done = 0;
    do i = 1 to 30 while (not done);
      if scan(own_numbers, i, ' ') ^= '' then do;
        count_own_numbers = i;
      end;
      else do;
        done = 1;
      end;
    end;
    call symput("count_own_numbers", compress(put(count_own_numbers, 16.)));
  end;
run;
%put &=count_winning_numbers;
%put &=count_own_numbers;

data WORK.scan;
  set WORK.input;
  length card_number 8
         wins        8
         points      8
  ;
  card_number = input(scan(inline, 2, ' :'), 8.);
  array winning{&count_winning_numbers.} w1-w&count_winning_numbers.;
  array own{&count_own_numbers.}         o1-o&count_own_numbers.;
  wins = 0;
  points = 0;
  do i=1 to &count_winning_numbers.;
    winning(i) = input(scan(scan(inline, 2, ':|'), i, ' '), 8.);
    do j=1 to &count_own_numbers.;
      own(j) = input(scan(scan(inline, 3, ':|'), j, ' '), 8.);
      if own(j) = winning(i) then wins = sum(wins, 1);
    end;
  end;
  if wins > 0 then do;
    points = 2**(wins-1);
  end;
run;

proc sql;
  create table WORK.SUM_POINTS as
  select sum(points) as POINTS_SUM
  from WORK.scan
  ;
quit;

data WORK.PART1;
  set WORK.SUM_POINTS(obs=1);
  put 'Sum of points: ' POINTS_SUM;
run;


