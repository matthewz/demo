usage() 
{
   printf "%s\n" "Usage: $ ./build.sh [ARG] [dir1 dir2 dir3]"
} 

initialization() 
{
   RC=0
   printf "%s\n"     "=====================================     Initialization            ============================="
   if [ ${DEBUG} -eq 1 ] ; then echo -n "PWD: " ; pwd ; echo "ls -al: " ; ls -al ; fi
   if [ -e "./.function" ] 
   then 
      . ./.function
   fi
   echo "CMD Line Args: '${@}'"
   if [ $LOCAL -eq 1 ] ; then . ./.var ; RC=$? ; show_local_vars ; fi
   if [ $RC -ne 0 ] ; then return $RC ; fi
   if [ $DEBUG -eq 1 ] ; then show_local_vars ; RC=$? ; fi
   if [ $RC -ne 0 ] ; then return $RC ; fi
   init_log_files ; RC=$?   
   if [ $RC -ne 0 ] ; then return $RC ; fi
   get_args "${@}" ; RC=$?
   if [ $RC -ne 0 ] ; then return $RC ; fi
   return $RC
}

processing() 
{
   printf "%s\n"     "=====================================       Processing           ============================"
   RC=0
   if [ -n "${DIRS}" ] 
   then
      if [[ "${BTYPE}" == "PY" ]] ; then build_component "${DIRS}" ; RC=$? ; fi
      if [ $RC -ne 0 ] ; then return $RC ; fi
   else
      echo "No DIRS found to process..."
   fi
   return $RC
}

termination() 
{
   printf "%s\n"     "=====================================       Termination         ============================="
   echo -n "PWD: " ; pwd
   set -x
   find build 
   set +x
   echo "logging accum's from log files..."
   if [ $1 -ne 0 ] ; then echo "Exited with return code: $1" ; return $1 ; fi
   echo "Exited normally with return code: $1"
   return 0
}

main()
{
   printf "\n\n%s\n" "================================================================================================="
   printf "%s\n"     "=====================================     Building Components    ================================"
   printf "%s\n\n"   "================================================================================================="
   echo
   RC=0
   initialization "${@}" ; RC=$?
   if [ $RC -eq 0 ] ; then processing "${@}" ; RC=$? ; fi
   termination $RC
   return $RC
}

DEBUG=0 ; LOCAL=0
main "${@}"
exit $?
