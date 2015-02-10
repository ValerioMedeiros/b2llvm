import os
import collections

# Basic functions
def filename():
    name = "ID"+"{:0>5d}".format(filename.count_name)
    filename.count_name+=1
    return name
filename.count_name=0

#Clean the screen
print ("\n"*100)
print("*****************************************************************")
print("* 1.0 Starting the generator of tests:                          *")
print("*****************************************************************")
#1.0 Open the file
myfile = open("B0_grammar_TestSet/b0_grammar_full.productionCoverage.1.11.out")
fullText = myfile.read()

#Declare functions
dic = collections.OrderedDict()
def add_dic(i,j):
    dic[i]=j
    
def replace_all():
    global fullText
    for i, j in dic.items():
        if( i in fullText):
            fullText = fullText.replace(i, j)
        else:
            print("ERROR: text not found to be replaced:"+i )



print("*****************************************************************")
print("* 2.0 Making the replaces                                       *")
print("*****************************************************************")
    
add_dic("IMPLEMENTATION ID ", "IMPLEMENTATION ID1 ")
add_dic("ID . ID", "ID.ID")
add_dic("SEES ID", "SEES COMPSEES")
add_dic("REFINES ID", "REFINES COMPREF_r")
add_dic("IMPORTS ID ID", "IMPORTS xxx.COMPIMP")
add_dic("INTLit", "0")
add_dic("CString", "\"Hello\"")
add_dic("CONCRETE_VARIABLES ID ", "CONCRETE_VARIABLES ID INITIALISATION ID :=1 ")
# Until this replaces the examples has syntax correct
add_dic("COMPIMP ( 0 ) ", "COMPIMP_INT ( 0 ) ")
add_dic("COMPIMP ( MAXINT ) ", "COMPIMP_INT ( 32767 ) ")
add_dic("COMPIMP ( MININT ) ", "COMPIMP_INT ( -32768 ) ")
add_dic("COMPIMP ( FALSE ) ", "COMPIMP_BOOL ( FALSE ) ")
add_dic("COMPIMP ( TRUE ) ", "COMPIMP_BOOL ( TRUE ) ")

#ID0008 
dec_rec ="CONCRETE_CONSTANTS const_rec PROPERTIES const_rec: struct( aa : INT) VALUES  const_rec =  rec( aa : 1) "
imp_rec = "REFINES COMPREF_r  IMPORTS xxx.COMPIMP_INT ( const_rec ' aa )"
add_dic("REFINES COMPREF_r IMPORTS xxx.COMPIMP ( ID ' ID ) ", dec_rec+imp_rec) 

#ID0012 
dec_rec ="CONCRETE_CONSTANTS const_rec, vec PROPERTIES const_rec: struct( aa : INT) &  vec = { 0|-> 0, 1|->1} VALUES  const_rec =  rec( aa : 1) ; vec = { 0|-> 0, 1|->1} "
imp_rec = "REFINES COMPREF_r  IMPORTS xxx.COMPIMP_INT (vec ( const_rec ' aa ))"
add_dic("REFINES COMPREF_r IMPORTS xxx.COMPIMP ( ID ( ID ' ID ) ) ", dec_rec+imp_rec) 

add_dic("IMPORTS xxx.COMPIMP ( 0 + 0 )","IMPORTS xxx.COMPIMP_INT ( 0 + 0 )")
add_dic("IMPORTS xxx.COMPIMP ( 0 - 0 )","IMPORTS xxx.COMPIMP_INT ( 0 - 0 )")
add_dic("IMPORTS xxx.COMPIMP ( - 0 )","IMPORTS xxx.COMPIMP_INT ( - 0 )")
add_dic("IMPORTS xxx.COMPIMP ( 0 * 0 )","IMPORTS xxx.COMPIMP_INT ( 0 * 0 )")
add_dic("IMPORTS xxx.COMPIMP ( 0 / 0 )","IMPORTS xxx.COMPIMP_INT ( 0 / 0 )")
add_dic("IMPORTS xxx.COMPIMP ( 0 mod 0 )","IMPORTS xxx.COMPIMP_INT ( 0 mod 0 )")
add_dic("IMPORTS xxx.COMPIMP ( 0 ** 0 )","IMPORTS xxx.COMPIMP_INT ( 0 ** 0 )")
add_dic("IMPORTS xxx.COMPIMP ( succ ( 0 ) )","IMPORTS xxx.COMPIMP_INT ( succ ( 0 ) )")
add_dic("IMPORTS xxx.COMPIMP ( pred ( 0 ) )","IMPORTS xxx.COMPIMP_INT ( pred ( 0 ) )")
add_dic("IMPORTS xxx.COMPIMP ( ( 0 ) )","IMPORTS xxx.COMPIMP_INT ( ( 0 ) )")

add_dic("IMPORTS xxx.COMPIMP ( rec","IMPORTS xxx.COMPIMP_REC ( rec")

infValue = "CONCRETE_CONSTANTS  vec  PROPERTIES     vec = { 0|-> 0, 1|->1} /* type */ VALUES     vec = { 0|-> 0, 1|->1}  /* value */"
orig = "REFINES COMPREF_r IMPORTS xxx.COMPIMP ( ID ( ID ) ) END"
new = "REFINES COMPREF_r IMPORTS xxx.COMPIMP_INT ( vec(0) ) "+  infValue + " END"
add_dic(orig , new)

add_dic("REFINES COMPREF_r PROMOTES ID END", "REFINES COMPIMP_op IMPORTS COMPIMP(NAT) PROMOTES do INITIALISATION var:= 0 END") # I did not found a solution.
add_dic("REFINES COMPREF_r EXTENDS ID.ID ( ID ) END","REFINES COMPREF_r EXTENDS xxx.COMPIMP_INT ( 0 ) END")
add_dic("SETS ID END" , "SETS simplerange VALUES simplerange = 0..3 END")
add_dic("SETS ID = { ID } END" , "SETS simpleset = { a0 } END")
add_dic("CONCRETE_CONSTANTS ID END" , "CONCRETE_CONSTANTS simpleconstant PROPERTIES simpleconstant : NAT VALUES simpleconstant = 1  END")
add_dic("CONSTANTS ID END" , "CONSTANTS simpleconstant PROPERTIES simpleconstant : NAT VALUES simpleconstant = 1  END")
add_dic("VALUES ID = ID", "CONSTANTS simpleconstant PROPERTIES simpleconstant : INT  VALUES simpleconstant = MAXINT")
add_dic("VALUES ID = Bool ( ID = ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL VALUES simplebool = bool ( MAXINT = MAXINT )")
add_dic("VALUES ID = Bool ( ID /= ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool = bool ( MAXINT /= MAXINT )")
add_dic("VALUES ID = Bool ( ID /= ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool = bool ( MAXINT /= MAXINT )")
add_dic("VALUES ID = Bool ( ID < ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool = bool ( MAXINT < MAXINT )")
add_dic("VALUES ID = Bool ( ID > ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool = bool ( MAXINT > MAXINT )")
add_dic("VALUES ID = Bool ( ID <= ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool = bool ( MAXINT <= MAXINT )")
add_dic("VALUES ID = Bool ( ID >= ID )","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool = bool ( MAXINT >= MAXINT )")
add_dic("VALUES ID = Bool ( ID = ID & ID = ID ) ","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool =  bool ( MAXINT = MAXINT & MININT = MININT )")
add_dic("VALUES ID = Bool ( ID = ID or ID = ID ) ","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool =  bool ( MAXINT = MAXINT or MININT = MININT )")
add_dic("VALUES ID = Bool ( not ( ID = ID ) ) ","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool =  bool ( not ( 0 = 1 ))")
add_dic("VALUES ID = Bool ( ( ID = ID ) ) ","CONSTANTS simplebool PROPERTIES simplebool : BOOL  VALUES simplebool =  bool ( not ( 0 = 1 ))")
add_dic("VALUES ID = 0 .. 0 ","CONSTANTS simpleset PROPERTIES simpleset <: NAT  VALUES simpleset = 0 .. 0 ")
add_dic("CONCRETE_VARIABLES ID INITIALISATION ID :=1 ", "CONCRETE_VARIABLES vari INVARIANT vari : INT INITIALISATION vari :=1 ")
add_dic("INITIALISATION BEGIN ID ( MAXINT ) := MAXINT END","CONCRETE_VARIABLES vari_array INVARIANT vari_array : 0..MAXINT --> NAT INITIALISATION BEGIN vari_array ( MAXINT ) := MAXINT END")

# Esta inicialização poderia é aplicada para todos os tipos ?
add_dic("INITIALISATION BEGIN ID := ID END","CONCRETE_VARIABLES vari_int INVARIANT vari_int : INT INITIALISATION BEGIN vari_int := 1 END")
add_dic("INITIALISATION BEGIN ID ' ID := MAXINT", "CONCRETE_VARIABLES var_rec INVARIANT var_rec : struct( aa : INT) INITIALISATION var_rec:= rec( aa : 1); BEGIN var_rec ' aa := MAXINT", )

#Added just the IMPORT clause to call an operation
add_dic("INITIALISATION BEGIN ID <-- ID ( MAXINT ) END", "IMPORTS COMPIMP(ID) CONCRETE_VARIABLES vari_int INVARIANT vari_int : INT INITIALISATION  BEGIN  vari_int <-- do_int ( MAXINT ) END")
add_dic("INITIALISATION BEGIN ID <-- ID ( \"Hello\" ) END END","IMPORTS COMPIMP(ID) CONCRETE_VARIABLES vari_int INVARIANT vari_int : INT INITIALISATION  BEGIN vari_int <-- do_string ( \"Hello\" ) END END")
add_dic("VAR ID IN skip END", "VAR var_temp IN var_temp:=1 END")
add_dic("INITIALISATION ID := bool ( ID = ID )", "CONCRETE_VARIABLES vari_bool INVARIANT vari_bool : BOOL INITIALISATION vari_bool := bool ( 0 = 0 )")
add_dic("INITIALISATION CASE ID OF EITHER ID THEN skip  ELSE skip END","CONCRETE_VARIABLES vari_bool INVARIANT vari_bool : BOOL INITIALISATION vari_bool:= FALSE; CASE vari_bool OF EITHER TRUE THEN skip  ELSE skip END")
add_dic("REFINES COMPREF_r OPERATIONS ID <-- ID ( ID ) = BEGIN skip END", "REFINES COMPIMP OPERATIONS do = BEGIN skip END; res <-- do_int (value)  =  BEGIN res := value + 0 END ; res <-- do_string (value)  = BEGIN res := 0 END")

# Remove examples with erros.
# It should be fixed by Cleverton. 

add_dic("IMPLEMENTATION ID1 ( ID ) REFINES COMPREF_r IMPORTS xxx.COMPIMP_REC ( rec ( ID : ID ) ) END\n","") #ID00023
add_dic("IMPLEMENTATION ID1 ( ID ) REFINES COMPREF_r IMPORTS xxx.COMPIMP_REC ( rec ( ID : { ID |-> MAXINT } ) ) END\n","")
add_dic("IMPLEMENTATION ID1 ( ID ) REFINES COMPREF_r IMPORTS xxx.COMPIMP_REC ( rec ( ID : ID * { MAXINT } ) ) END\n","")
add_dic("IMPLEMENTATION ID1 ( ID ) REFINES COMPREF_r IMPORTS xxx.COMPIMP_REC ( rec ( ID : ID ) ' ID ) END\n","")
add_dic("IMPLEMENTATION ID1 ( ID ) REFINES COMPREF_r PROPERTIES 0 = FALSE END\n","") #ID00040
add_dic("IMPLEMENTATION ID1 ( ID ) REFINES COMPREF_r PROPERTIES 0 = TRUE END\n", "") #ID00041
#add_dic("","")
#add_dic("","")


replace_all()



print("*****************************************************************")
print("* 3.0 Generating the new file tests                             *")
print("*****************************************************************")
myfile = open("B0_grammar_TestSet/GeneratedTestsFull.txt","w")
myfile.write(fullText)
myfile.close()
#3.1 Print in several files
setOfTest = fullText.split("\n")
setOfTest.pop(-1)#Remove the last element that is empty

nTests = len(setOfTest)
for c in range(0,nTests):
    n = filename()
    #replace the name of file
    setOfTest[c]=setOfTest[c].replace("ID1",n)
    #print(   setOfTest[c])
    myfile = open("B0_grammar_TestSet/"+n+".imp","w")
    myfile.write(setOfTest[c])
    myfile.close()


print("*****************************************************************")
print("* 4.0 Calling the BXML                                          *")
print("*****************************************************************")
#pBXML = "/Applications/AtelierB.app/AB/bbin/macosx/bxml"
pBXML = "./bxml"
pProject = "./B0_grammar_TestSet/"
pOut = "./out/"


filename.count_name=0
oks=0
for test in setOfTest:
    n = filename()
# B0Checher
#    command = pBXML+' -c  -i4 -I '+ pProject + ' -O'+pOut+' '+pProject+n+'.imp '
    command = pBXML+' -a  -i4 -I '+ pProject + ' -O'+pOut+' '+pProject+n+'.imp '
    print(n)
#    print(command)

    f = os.popen(command)
    res = f.read()
    if len(res)>3:
        print(test)        
        print(res)
    else:
        oks+=1
        #print(test) 
        print(" OK ")

print("Tests b0 checked: "+str(oks) + " and total tests:"+str(len(setOfTest)) )


print("*****************************************************************")
print("* 5.0 Calling the B2LLVM                                        *")
print("*****************************************************************")


print("*****************************************************************")
print("* 6.0 Calling the C4B                                           *")
print("*****************************************************************")

filename.count_name=oks=0
for test in setOfTest:
    n = filename()
    command = './b2c  -I '+ pProject + ' -C ./out_C '+pProject+n+'.imp '
    print(n)
    #print(command)
    f = os.popen(command)
    res = f.read()
    if "error:" in res :
        print ("Error : "+test+"\n"+res)
    else:
        oks+=1
        print("OK")
    
print("Tests b2c generated: "+str(oks) + " and total tests:"+str(len(setOfTest)) )
   
