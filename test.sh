!/bin/bash -l
# Batch script to run a serial job on Legion with the upgraded
# software stack under SGE.
# 1. Force bash as the executing shell.
$ -S /bin/bash
# 2. Request ten minutes of wallclock time (format hours:minutes:seconds).
$ -l h_rt=0:1:0
# 3. Request 1 gigabyte of RAM 
$ -l mem=1G
# 4. Request 15 gigabyte of TMPDIR space (default is 10 GB)
$ -l tmpfs=1G
# 5. Set the name of the job.
$ -N Heidi_Test
# 6. Set the working directory to somewhere in your scratch space.  This is
# a necessary step with the upgraded software stack as compute nodes cannot
# write to $HOME.
# Replace "<your_UCL_id>" with your UCL user ID :)
$ -wd /home/uceshhu/Scratch/output
# 7. Your work *must* be done in $TMPDIR 
cd $TMPDIR
# 8. Run the application.
/bin/date > date_in_tmpdir.txt
# 9. Preferably, tar-up (archive) all output files onto the shared scratch area
tar zcvf $HOME/Scratch/files_from_job_$JOB_ID.tar.gz $TMPDIR
# Make sure you have given enough time for the copy to complete!