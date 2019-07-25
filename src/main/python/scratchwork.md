# Which tables are affected by the Termination date / status?
- Attendance
- Department Salary
- Staff Salary
- Salary Summary ??? its department wise


# How to store termination date??? 
- make a separate table for it???
- add it to the employee table?

# DOnt need to manually do begin or insert rows since rowcount is selfupdating.
- only need to filter from emplist thats it

#bug on exit due to improper object destruction order
- QBasicTimer::start: QBasicTimer can only be used with threads started with QThread
- to replicate change employee working status from the table and exit app

# When to not display terminated employee data:
- when the termination date is earlier than the earliest date being displayed by the model. like for attendance
- if the half is set to be 0 and month is Jan-2019 then DONT display employee if termination date is before 01-01-2019 or 
- if half is 1 and month is Feb-2019 then DONT display employee data if termination date is before 15-02-2019, OTHERWISE
- display as normal



# What if we just hide the row which has employee status as terminated, rather than filtering out employee / deleting from list etc..
- nevermind its only for tableviews not models. and it wouldnt make sense to keep terminated employees in the currently active emp list


# automatically set all attendance to absent , 0 for dates after termination date IF the termination date is within the current display range???? (QOL UPDATE)