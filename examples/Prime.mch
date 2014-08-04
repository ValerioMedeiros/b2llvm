MACHINE  Prime
DEFINITIONS
 SET_PREF_MAXINT == 20;
 SET_PREF_MAX_OPERATIONS == 200
OPERATIONS
  rr <-- IsPrime(xx) = PRE xx:NAT & xx>1 THEN
      IF #dd.(dd:NAT & dd>1 & dd<xx & xx mod dd = 0) THEN
        rr := FALSE
      ELSE
        rr := TRUE
      END 
   END
END