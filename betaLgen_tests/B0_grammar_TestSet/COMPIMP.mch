MACHINE COMPIMP ( ID )

OPERATIONS
    do =
    BEGIN
        skip
    END;
    res <-- do_int (value)  =
    PRE value : INT THEN
    	res := value + 0
    END;

    res <-- do_string (value)  =
    PRE value : STRING THEN
    	res := 0 
    END


END
