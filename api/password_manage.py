from datetime import datetime

sample = ['h','+','=','i','j','k','l','m','>','n','o','p','q','r','s','!','@','(',')',
              't','u','v','w','{','}','x','y','z','?','a','b',',','c','d','e','f','g','#','$','-','_',
              'A','B',':','C','\\','D','E','\"','F','G','|','P','Q','R','S','%','^',
              'T','U','<','V','W','\'','X','Y',';','Z','/','H','I','J','`','K','L','~','M','.',
              'N','O','&','*','1','2','3','4','5','6','7','8','9','0'
              ]

l = len(sample)

def encrypt(password):
    length = len(password)
    if length<5:
        raise Exception("Sorry, minimum length is 5")
    
    a = datetime.now().hour
    b = datetime.now().minute
    
    mid = length//2
    encoded_pass = ''
        # create the list of characters

    for i in range(0,length):
        # If the position is the center of the string   
        # Adding a and b in the middle of pass
        if(i == mid):
            c1 = sample[a]
            encoded_pass += c1
            c2 = sample[b]
            encoded_pass += c2
            
        # enoding char
        j = i+1
        step  = sample.index(password[i])

        if(j%2==1):
            step += a
            step = step%l
            encoded_pass += sample[step]
        else:
            step += b
            step = step%l
            encoded_pass += sample[step]
        
        
    return encoded_pass

def decode( encoded_pass):
    decoded_pass = ''
    length = len(encoded_pass)
    mid = length//2
    a = encoded_pass[mid-1]
    b = encoded_pass[mid]
    a1 = sample.index(a)
    b1 = sample.index(b)

    for i in range(0,length):
            # Skipping encrypt key elements which are in middle
        if(i==mid-1 or i==mid):
            continue
            
            #Decoding char
        j = i+1
        if(j%2==1):
            c1 = sample.index(encoded_pass[i])
            calc = ((c1-a1)+l)%l
            #formula
            decoded_pass += sample[calc]
        else:
            c2 = sample.index(encoded_pass[i])
            calc = ((c2-b1)+l)%l
            decoded_pass += sample[calc]
        
    return decoded_pass

def check_password(db_pass,given_pass):
    if decode(db_pass)==given_pass:
        return True
    else:
        return False