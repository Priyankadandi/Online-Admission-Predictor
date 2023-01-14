from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from joblib import load
import re
from django.template.defaulttags import register


model = load('./savedModels/model.joblib')

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("login successful")
            return render(request, 'home.html')
        else:
            messages.info(request,"Invalid credentials")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html') 

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
      
        fnmregex = re.compile(r'^([a-z]+)([a-z]+)$', re.IGNORECASE)
        lnmregex = re.compile(r'^([a-z]+)([a-z]+)$', re.IGNORECASE)
        emailregex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        unmregex = re.compile(r'^[A-Za-z][A-Za-z0-9_]{7,29}$', re.IGNORECASE)
        passwdregex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$')

        if re.fullmatch(fnmregex, first_name):
            if re.fullmatch(lnmregex, last_name):
                if re.fullmatch(emailregex, email):
                    if re.fullmatch(unmregex, username):
                        if re.fullmatch(passwdregex, password1):
                            if password1==password2:
                                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                                    messages.info(request, "Email id or username already registered")
                                    return render(request, 'register.html')
                                else:
                                    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password1)
                                    user.save()
                                    print('User created')
                                    return render(request, 'login.html')
                            else:
                                messages.info(request, "Password not matching")
                                return render(request, 'register.html')
                        else:
                            messages.info(request, "Enter valid password")
                            return render(request, 'register.html')
                    else:
                        messages.info(request, "Enter valid username")
                        return render(request, 'register.html')
                else:
                    messages.info(request, "Enter valid Email Id")
                    return render(request, 'register.html')
            else:
                messages.info(request, "Enter valid Last Name")
                return render(request, 'register.html')
        else:
            messages.info(request, "Enter valid First Name")
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')

def home(request):
    college = {1: ["AARM","AAR MAHAVEER ENGINEERING COLLEGE" ,"BANDLAGUDA"],
               2: ["ACEG","A C E ENGINEERING COLLEGE (AUTONOMOUS)","GHATKESAR"],
               3: ["AITH","ANNAMACHARYA INST OF TECHNOLOGY AND SCI", "HAYATHNAGAR"],
               4: ["AIZA","AIZZA COLLEGE OF ENGG AND TECHNOLOGY", "MANCHERIAL"], 
               5: ["AKIT","ABDULKALAM INST OF TECHNOLOGY AND SCI", "KOTHAGUDEM"], 
               6: ["ANRH","ANURAG COLLEGE OF ENGINEERING", "GHTKESAR"], 
               7: ["ANRK","ANURAG ENGINEERING COLLGE", "KODAD"], 
               8: ["ANWP","ANWAR-ULOOM COLLEGE  OF PHARMACY", "HYDERABAD"], 
               9: ["ARJN","ARJUN COLLEGE OF TECHNOLOGY AND SCIENCE", "BATASINGARAM"], 
               10: ["ASRA","AVANTHIS SCIENTIFIC TECH AND RESEARCH ACADEMY", "HAYATHNAGAR"], 
               11: ["AURG","AURORAS SCIENTIFIC AND TECHNOLOGICAL INSTITUTE", "GHATKESAR"], 
               12: ["AURH","RAMAPPA ENGINEERING COLLEGE", "HANAMKONDA"], 
               13: ["AURP","AURORAS TECHNOLOGICAL AND  RESEARCH INSTITUTE", "PARVATHAPUR"], 
               14: ["AVHP","AVANTHI INST OF PHARMSCI", "HAYATHNAGAR"], 
               15: ["AVIH","AVANTHI INST OF ENGG AND TECHNOLOGY", "HAYATHNAGAR"], 
               16: ["AVNI","AVN INST OF ENGG TECHNOLOGY", "IBRAHIMPATAN"], 
               17: ["BIET","BHARAT INSTITUTE OF ENGG AND TECHNOLOGY", "IBRAHIMPATNAM"], 
               18: ["BITN","BALAJI INSTITUTE OF TECHNOLOGY AND SCI", "NARSAMPET"], 
               19: ["BNPW","BOJJAM NARASIMHULU PHARM COLL FOR WOMEN", "SAIDABAD"], 
               20: ["BOMA","BOMMA INST OF TECHNOLOGY AND SCI", "KHAMMAM"], 
               21: ["BOSE","ANU BOSE INSTT OF TECHNOLOGY", "PALONCHA"], 
               22: ["BPCP","BHASKAR PHARMACY COLLEGE", "YENKAPALLY"], 
               23: ["BREW","BHOJREDDY ENGINEERING COLLEGE FOR WOMEN", "SAIDABAD"], 
               24: ["BRIG","BRILLIANT GRAMMER SCHOOL EDNL SOC GRP OF INSTNS","HAYATHNAGAR"], 
               25: ["BRIL","BRILLIANT INSTT OF ENGG AND TECHNOLOGY", "HAYATHNAGAR"], 
               26: ["BSGP","BANDARI SRINIVAS INSTITUTE OF TECHNOLOGY", "CHEVELLA"], 
               27: ["BSKR","BHASKAR ENGINEERING COLLEGE", "YENKAPALLY"], 
               28: ["BVRI","B V RAJU INSTITUTE OF TECHNOLOGY", "NARSAPUR"], 
               29: ["BVRW","BVRIT COLLEGE OF ENGINEERING FOR WOMEN", "BACHUPALLY"], 
               30: ["CASR","COLLEGE OF AGRICULTURAL ENGG", "SANGAREDDY"], 
               31: ["CBIT","CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY", "GANDIPET"],
               32: ["CDTK","COLLEGE OF DAIRY TECHNOLOGY", "KAMAREDDY"],
               33: ["CFSR","COLLEGE OF FOOD SCIENCE AND TECHNOLOGY", "RUDRUR"],
               34: ["CHET","SRI CHAITANYA COLLEGE OF ENGG AND TECH", "IBRAHIMPATAN"], 
               35: ["CHTN","SREE CHAITANYA COLLEGE OF ENGINEERING", "KARIMNAGAR"], 
               36: ["CHTS","SREE CHAITANYA INST OF TECHNOLOGY SCIENCES", "KARIMNAGAR"], 
               37: ["CITS","CHAITANYA INST OF TECH AND SCIENCE", "HANAMKONDA"], 
               38: ["CJIT","CHRISTU JYOTHI INSTITUTE OF TECHNOLOGY AND SCI", "JANGAON"], 
               39: ["CMRG","CMR TECHNICAL CAMPUS (AUTONOMOUS)", "KANDLAKOYA"], 
               40: ["CMRK","C M R COLLEGE OF ENGG AND TECHNOLOGY", "KANDLAKOYA"], 
               41: ["CMRM","CMR INSTITUTE OF TECHNOLOGY AUTONOMOUS", "KANDLAKOYA"], 
               42: ["CMRN","CMR ENGG COLLEGE", "KANDLAKOYA"], 
               43: ["CMRP","C M R COLL OF PHARMACY", "KANDLAKOYA"], 
               44: ["CVRH","CVR COLLEGE OF ENGINEERING", "IBRAHIMPATAN"], 
               45: ["CVSR","ANURAG UNIVERSITY  (FORMERLY ANURAG GRP OF INSTNS- CVSR COLL OF ENGG)", "GHATKESAR "], 
               46: ["DCET","DECCAN COLLEGE OF ENGINEERING AND TECHNOLOGY", "DARUSSALAM"], 
               47: ["DIPS","DHANVANTHARI INST OF PHARM SCI", "KOTHAGUDEM"], 
               48: ["DRKC","D R K COLLEGE OF ENGINEERING AND TECHNOLOGY", "BOWRAMPET"], 
               49: ["DRKI","D R K INSTITUTE OF SCI AND TECHNOLOGY", "BOWRAMPET"], 
               50: ["DSOP","DECCAN SCHOOL OF PHARMACY", "NAMPALLY"], 
               51: ["ELEN","ELLENKI COLLGE OF ENGG AND TECHNOLOGY", "PATANCHERU"], 
               52: ["GATE","GATE INSTITUTE OF TECHNOLOGYAND SCIENCES", "KODAD"], 
               53: ["GCPK","GEETHANJALI COLL OF PHARM", "KEESARA"], 
               54: ["GCTC","GEETANJALI COLLEGE OF ENGG AND TECHNOLOGY", "KEESARA"], 
               55: ["GLND","GLAND INST OF PHARACEUTICAL SCIENCES", "KOTHAPET"], 
               56: ["GLOB","GLOBAL INST OF ENGINEERING AND TECHNOLOGY", "CHILKUR"], 
               57: ["GNIT","GURUNANAK INST OF TECHNOLOGY", "IBRAHIMPATAN"], 
               58: ["GNPT","GANAPATHI ENGINEERING COLLGE", "WARANGAL"], 
               59: ["GNTW","G NARAYNAMMA INSTITUTE OF TECHNOLOGY AND SCI", "RAYADURG"], 
               60: ["GPRP","G P R COLLEGE OF PHARMACY", "MEHDIPATNAM"], 
               61: ["GRCP","GOKARAJU RANGARAJU COLLEGE OF PHARMACY", "BACHUPALLI"],
               62: ["GRRR","GOKARAJU RANGARAJU INSTITUTE OF ENGG AND TECH", "MIYAPUR"],
               63: ["GURU","GURUNANAK INSTTECH CAMPUS", "IBRAHIMPATAN"],
               64: ["HITM","HYDERABAD INST OF TECHNOLOGY AND MGMT", "MEDCHAL"], 
               65: ["HOLY","HOLY MARY INSTITUTE OF TECH SCIENCE", "KEESARA"], 
               66: ["IARE","INSTITUTE OF AERONAUTICAL ENGINEERING", "DUNDIGAL"], 
               67: ["IITT","INDUR INSTITUTE OF ENGINEERING AND TECHNOLOGY", "SIDDIPET"], 
               68: ["INDI","SRI INDU INSTITUTE OF ENGINEERING AND TECHNOLOGY", "IBRAHIMPATAN"], 
               69: ["INDU","SRI INDU COLLEGE OF ENGG AND TECHNOLOGY", "IBRAHIMPATAN"], 
               70: ["ISLC","ISL ENGINEERING COLLEGE", "BANDLAGUDA"], 
               71: ["JANG","JANGOAN INSTITUTE OF PHARMACEUTICAL SCIS", "JANGAON"], 
               72: ["JAYA","JAYAMUKHI INSTITUTE OF TECHNOLOGY AND SCIS", "NARSAMPET"], 
               73: ["JBIT","J B INSTITUTE OF ENGG AND TECHNOLOGY", "YENKAPALLY"], 
               74: ["JMTK","JYOTHISHMATHI INST OF TECHNOLOGY SCIENCES", "KARIMNAGAR"], 
               75: ["JMTS","JYOTHISHMATHI INSTITUTE OF TECHNOLOGY AND SCI", "KARIMNAGAR"], 
               76: ["JNKR","JNTU COLLEGE OF ENGINEERING  KARIMNAGAR", "KARIMNAGAR"], 
               77: ["JNPASF","JNTU SCHOOL OF PLANNING AND ARCH - SELF FINANCE", "MASABTANK"], 
               78: ["JNTH","JNTU COLLEGE OF ENGG  HYDERABAD", "HYDERABAD"], 
               79: ["JNTHMT","JNTUH-5 YEAR INTEGRATED MTECH  SELF FINANCE", "KUKATPALLY"], 
               80: ["JNTM","JNTUH COLLEGE OF ENGG  MANTHANI", "MANTHANI"], 
               81: ["JNTS","J N T U COLLEGE OF ENGINEERING  SULTANPUR", "SULTANPUR"], 
               82: ["JOGI","JOGINPALLY B R ENGINEERING COLLEGE", "YENKAPALLY"], 
               83: ["JPNE","JAYA PRAKASH NARAYAN COLLEGE OF ENGINEERING", "MAHABUBNAGAR"], 
               84: ["KCEA","KSHATRIYA COLLEGE OF ENGINEERING", "ARMOOR"], 
               85: ["KDDW","KODADA INST OF TECHNOLOGY AND SCIENCE FOR WOMEN", "KODADA"], 
               86: ["KGRH","KGREDDY COLLEGE OF ENGG AND TECHNOLOGY", "MOINABAD"], 
               87: ["KHMP","KHAMMAM COLLEGE OF PHARMACY", "KHAMMAM"], 
               88: ["KITS","KAKATIYA INSTITUTE OF TECHNOLOGY AND SCI", "WARANGAL"], 
               89: ["KITW","KAKATIYA INST OF TECHNOLOGY SCI FOR WOMEN", "NIZAMABAD"], 
               90: ["KLRT","KLRCOLLEGE OF ENGG AND TECHNOLOGY PALONCHA", "PALONCHA"], 
               91: ["KMIT","KESHAV MEMORIAL INST OF TECHNOLOGY", "NARAYANAGUDA"],
               92: ["KMTS","KHAMMAM INST OF TECHNOLOGY AND SCIENCE", "KHAMMAM"],
               93: ["KNRR","KASIREDDY NARAYANAREDDY COLL ENGG RES", "HAYATHNAGAR"],
               94: ["KPRT","KOMMURI PRATAP REDDY INST OF TECHNOLOGY", "GHATKESAR"], 
               95: ["KTKM","KAMALA INSTITUTE OF TECHNOLOGY AND SCIENCE", "HUZURABAD"], 
               96: ["KUCE","K U COLLEGE OF ENGG  KOTHAGUDEM", "KOTHAGUDEM"], 
               97: ["KUCESF","K U COLLEGE OF ENGG  KOTHAGUDEM", "KOTHAGUDEM"], 
               98: ["KUCP","K U COLLEGE OF PHARMACEUTICAL SCIENCES", "WARANGAL"], 
               99: ["KUEWSF","UNIVERSITY COLLEGE OF ENGG AND TECH FOR WOMEN KU CAMPUS", "WARANGAL"], 
               100: ["KUWL","KU COLLEGE OF ENGINEERING  AND TECHNOLOGY", "WARANGAL"], 
               101: ["LRDS","LORDS INSTITUTE OF ENGINEERING AND TECHNOLOGY", "HIMAYATSAGAR"], 
               102: ["MECS","MATRUSRI ENGINEERING COLLEGE", "HYDERABAD"], 
               103: ["MESP","MESCO COLLEGE OF PHARMACY", "MUSTAIDPURA"], 
               104: ["METH","METHODIST COLLEGE OF ENGINEERING AND TECHNOLOGY", "ABIDS"], 
               105: ["MGHA","MEGHA INST OF ENGG AND TECHNOLOGY FOR WOMEN", "GHATKESAR"], 
               106: ["MGIT","MAHATMA GANDHI INSTITUTE OF TECHNOLOGY", "GANDIPET"], 
               107: ["MGUNSF","MGU COLLEGE OF ENGINEERING AND TECHNOLOGY", "NALGONDA"], 
               108: ["MHVR","MAHAVEER INSTITUTE OF SCI AND TECHNOLOGY", "BANDLAGUDA"], 
               109: ["MINA","MINA INST OF ENGG AND TECHNOLOGY FOR WOMEN", "MIRYALAGUDA"], 
               110: ["MIPM","MOONRAY INST OF PHARM SCI", "RAIKAL"], 
               111: ["MJCT","M J COLLEGE OF ENGINEERING AND TECHNOLOGY", "BANJARA HILLS"], 
               112: ["MLID","M L R INSTITUTE OF TECHNOLOGY", "DUNDIGAL"], 
               113: ["MLRD","MALLA REDDY COLLEGE OF ENGG  TECHNOLOGY (AUTONOMOUS)", "MYSAMMAGUDA"], 
               114: ["MLRP","MARRI LAXMAN REDDY INSTITUTE OF PHARMACY", "DUNDIGAL"], 
               115: ["MLRS","MARRI LAXMAN REDDY INST OF TECHNOLOGY AND MANAGEMENT (AUTONOMOUS)", "DUNDIGAL"], 
               116: ["MMTZ","MUMTAZ COLL OF ENGG TECHNOLOGY", "HYDERABAD"], 
               117: ["MNRP","M N R COLLEGE OF PHARMACY", "SANGAREDDY"], 
               118: ["MNRT","MNRCOLLEGE OF ENGINEERING AND TECHNOLOGY", "SANGAREDDY"], 
               119: ["MOTK","MOTHER TERESA INSTITUTE OF SCI AND TECHNOLOGY", "SATHUPALLY"], 
               120: ["MRCE","MALLA REDDY COLLEGE OF ENGINEERING", "MYSAMMAGUDA"], 
               121: ["MRCP","MALLA REDDY COLLEGE OF PHARMACY", "MAISAMMAGUDA"],
               122: ["MRCW","MALLA REDDY ENGG COLLEGE FOR WOMEN (AUTONOMOUS)", "MAISAMMAGUDA"],
               123: ["MREC","MALLAREDDY ENGINEERING COLLEGE", "MAISAMMAGUDA"],
               124: ["MREM","MALLA REDDY ENGINEERING COLLEGE AND MANAGEMENT SCIENCES", "MEDCHAL"], 
               125: ["MRET","MALLAREDDY INST OF ENGG AND TECHNOLOGY", "MAISAMMAGUDA"], 
               126: ["MREW","MALLA REDDY COLLEGE OF ENGINEERING FOR WOMEN", "MAISAMMAGUDA"], 
               127: ["MRIT","MALLAREDDY INST OF TECHNOLOGY AND SCI", "MAISAMMAGUDA"], 
               128: ["MRPC","MALLA REDDY PHARMACY COLLEGE", "MAISAMMAGUDA"], 
               129: ["MRTN","ST MARTINS ENGINEERING COLLEGE AUTONOMOUS", "DHULAPALLY"], 
               130: ["MTEC","MOTHER THERESA COLLEGE OF ENGG AND TECHNOLOGY", "PEDDAPALLY"], 
               131: ["MVSR","M V S R ENGINEERING COLLEGE", "NADERGUL"], 
               132: ["NAWB","NAWAB SHAH ALAM KHAN COLL OF ENGG AND TECH", "NEW MALAKPET"], 
               133: ["NGIT","NEIL GOGTE INST OF TECHNOLOGY", "KACHIVANI SINGARAM"], 
               134: ["NGMA","NIGAMA ENGINEERING COLLEGE", "KARIMNAGAR"], 
               135: ["NIET","NETAJI INSTITUTE OF ENGINEERING AND TECHNOLOGY", "CHOUTUPPAL"], 
               136: ["NNRG","NALLA NARASIMHA REDDY EDNL SOC GRP OF INSTNS", "GHATKESAR"], 
               137: ["NOVH","NOVA COLLEGE OF ENGINEERING & TECHNOLOGY", "BATASINGARAM"], 
               138: ["NRCM","NARSIMHAREDDY ENGINEERING COLLEGE", "MAISAMMAGUDA"], 
               139: ["NREC","NALLAMALLA REDDY ENGINEERING COLLEGE", "GHATKESAR"], 
               140: ["OUCE","O U COLLEGE OF ENGG  HYDERABAD", "HYDERABAD"], 
               141: ["OUCT","O U COLLEGE OF TECH  HYDERABAD", "HYDERABAD"], 
               142: ["PALV","PALLAVI ENGINEERING COLLEGE", "KUNTLOOR"], 
               143: ["PETW","PRINCETON INST OF ENGG TECH FOR WOMEN", "GHATKESAR"], 
               144: ["PLMU","PALAMUR UNIVERSITY", "MAHABUBNAGAR"], 
               145: ["PRIW","PRIYADARSHINI INSTITUTE OF SCIENCE & TECHNOLOGY FOR WOMEN", "KHAMMAM"], 
               146: ["PURD","PULLA REDDY INST OF PHARMACY DINDIGUL", "DUNDIGAL"], 
               147: ["RITW","RISHI MS INST OF ENGG AND TECH FOR WOMEN", "KUKATPALLY"], 
               148: ["SAIS","SAI SPURTI INSTITUTE OF TECHNOLOGY", "SATHUPALLY"], 
               149: ["SANA","SANA  ENGINEERING COLLEGE", "KODADA"], 
               150: ["SANP","SANA COLLEGE OF PHARMACY", "KODAD"], 
               151: ["SBIT","SWARNA BHARATHI INSTITUTE OF SCI AND TECHNOLOGY", "KHAMMAM"],
               152: ["SCET","SHADHAN COLL OF ENGINEERING AND TECHNOLOGY", "PEERANCHERU"],
               153: ["SCOP","SHADAN COLLEGE OF PHARMACY", "PEERANCHERU"],
               154: ["SDCP","SURABHI DAYAKAR RAO COLLEGE OF PHARMACY", "GAJWEL"], 
               155: ["SDES","SRI DATTA COLL OF ENGINEERING AND SCIENCE", "IBRAHIMPATAN"], 
               156: ["SDEW","SRIDEVI WOMENS ENGINEERING COLLEGE", "GANDIPET"], 
               157: ["SDGI","SREE DATTHA GRP OF INSTNS", "IBRAHIMPATAN"], 
               158: ["SIEI","SIDDHARTHA INSTT OF ENGG AND TECHNOLOGY", "IBRAHIMPATAN"], 
               159: ["SISG","SIDDHARTHA INSTT OF TECHNOLOGY AND SCIENCES", "GHATKESAR"], 
               160: ["SMCD","ST  MARYS ENGINEERING COLLEGE", "DESHMUKHI"], 
               161: ["SMED","ST  MARYS GROUP OF INSTITUTIONS", "DESHMUKHI"], 
               162: ["SMIC","ST MARYS INTEGRATED CAMPUS", "DESHMUKHI"], 
               163: ["SMSK","SAMSKRUTHI COLLEGE OF ENGG AND TECHNOLOGY", "GHATKESAR"], 
               164: ["SNIS","SREENIDHI INSTITUTE OF SCI AND TECHNOLOGY", "GHATKESAR"], 
               165: ["SNTI","SCIENT INSTITUTE OF TECHNOLOGY", "IBRAHIMPATAN"], 
               166: ["SNVM","S N VANITHA PHARMACY MAHA VIDYALAYA", "TARNAKA"], 
               167: ["SPEC","ST PETERS ENGINEERING COLLEGE AUTONOMOUS", "MEDCHAL"], 
               168: ["SPHN","SPHOORTHY ENGINEERING COLLEGE", "NADERGUL"], 
               169: ["SPKG","SAMSKRUTHI COLLEGE OF PHARMACY", "GHATKESAR"], 
               170: ["SRHP","S R UNIVERSITY ( FORMERLY S R ENGINEERING COLLEGE)", "HASANPARTHY"], 
               171: ["SRIW","SUMATHI REDDY INST OF TECHNOLOGY FOR WOMEN", "HASANPARTHY"], 
               172: ["SRYS","SREYAS INST OF ENGG AND TECHNOLOGY", "NAGOLE"], 
               173: ["STLW","STANLEY COLLEGE OF ENGG AND TECHNOLOGY FOR WOMEN", "ABIDS"], 
               174: ["SUUP","SULTAN UL-ULOOM COLLEGE OF PHARMACY", "BANJARA HILLS"], 
               175: ["SVES","SRI VENKATESWARA ENGINEERING COLLEGE", "SURYAPETA"], 
               176: ["SVHU","SATAVAHANA UNIVERSITY", "KARIMNAGAR"], 
               177: ["SVIT","SWAMI VIVEKANANDA INST OF TECHNOLOGY", "SECUNDERABAD"], 
               178: ["SVSE","SVS GRP OF INSTNS - SVS INST OF TECH", "HANAMKONDA"], 
               179: ["SWET","SHADHAN WOMENS COLL OF ENGG AND TECHNOLOGY", "KHAIRTABAD"], 
               180: ["SWIT","SWATHI INST OF TECHNOLOGY SCI", "HAYATHNAGAR"], 
               181: ["TALP","TALLA PADMAVATHI COLLEGE OF PHARMACY", "WARANGAL"],
               182: ["TCEK","TRINITY COLLEGE OF ENGINEERING AND TECHNOLOGY", "PEDDAPALLY"],
               183: ["TCTK","TRINITY COLLEGE OF ENGINEERING AND TECHNOLOGY", "KARIMNAGAR"],
               184: ["TKEM","TEEGALA KRISHNA REDDY ENGINEERING COLLEGE", "MIRPET"], 
               185: ["TKRC","T K R COLLEGE OF ENGG AND TECHNOLOGY (AUTONOMOUS)", "MIRPET"], 
               186: ["TKRP","TEEGALA KRISHNA REDDY COLLEGE OF PHARMACY", "MIRPET"], 
               187: ["TMLP","TIRUMALA COLL OF PHARMACY", "NIZAMABAD"], 
               188: ["TPCE","TALLA PADMAVATHI COLL OF ENGINEERING", "KAZIPET"], 
               189: ["TRRC","T R R COLLEGE OF ENGINEERING", "PATANCHERU"], 
               190: ["VAGE","VAAGDEVI COLLEGE OF ENGINEERING", "WARANGAL"], 
               191: ["VAGP","VAGDEVI COLLEGE OF PHARMACY", "HANAMKONDA"], 
               192: ["VASV","VASAVI COLLEGE OF ENGINEERING", "HYDERABAD"], 
               193: ["VBEC","VIGNANA BHARATHI ENGINEERING COLLEGE", "IBRAHIMPATAN"], 
               194: ["VBIT","VIGNANA BHARATHI INSTITUTE OF TECHNOLOGY (AUTONOMOUS)", "GHATKESAR"], 
               195: ["VCET","VISWESWARAYA COLL OF ENGG AND TECHNOLOGY", "IBRAHIMPATAN"], 
               196: ["VCOP","SRI VENKATESWARA COLLEGE OF PHARMACY", "MADHAPUR"], 
               197: ["VCPN","VIJAY COLL OF PHARMACY", "NIZAMABAD"], 
               198: ["VGNT","VIGNAN INSTITUTE OF TECHNOLOGY AND SCI", "DESHMUKHI"], 
               199: ["VGSE","VAAGESHWARI COLL OF ENGINEERING", "KARIMNAGAR"], 
               200: ["VGSP","VAAGESWARI COLLEGE OF PHARMACY", "KARIMNAGAR"], 
               201: ["VGWL","VAGDEVI ENGINEERING COLLEGE", "WARANGAL"], 
               202: ["VISA","VATHSALYA INSTITUTE OF SCI AND TECHNOLOGY", "BHONGIR"], 
               203: ["VITH","VINUTHNA INST OF TECHNOLOGY SCIENCE", "HASANPARTHY"], 
               204: ["VITS","SRI VISHWESWARAYA INST OF TECHNOLOGY AND SCI", "MAHABUBNAGAR"], 
               205: ["VJEC","V N R VIGNAN JYOTHI INSTITUTE OF ENGG AND TECH", "BACHUPALLY"], 
               206: ["VJIT","VIDYAJYOTHI INSTITUTE OF TECHNOLOGY", "MOINABAD"], 
               207: ["VJYA","VIJAYA ENGINEERING COLLEGE", "KHAMMAM"], 
               208: ["VJYH","VIJAYA COLLEGE OF PHARMACY", "HAYATHNAGAR"], 
               209: ["VKSP","VIKAS COLL OF PHARMACEUTICAL SCIENCES", "SURYAPET"], 
               210: ["VMEG","VARDHAMAN COLLEGE OF ENGINEERING", "SHAMSHABAD"], 
               211: ["VMTW","VIGNANS INST OF MANAGEMENT AND TECH FOR WOMEN", "GHATKESAR"], 
               212: ["VPRG","VISION COLLEGE OF PHARMSCI AND RES", "BODUPPAL"], 
               213: ["VREC","VIJAYA RURAL ENGINEERING COLLEGE", "NIZAMABAD"], 
               214: ["VRKW","DR VRK WOMENS COLL OF ENGG AND TECHNOLOGY", "MOINABAD"], 
               215: ["VSNU","VISHNU INST OF PHARM EDN AND RESEARCH", "VISHNUPUR"], 
               216: ["VVKN","VIVEKANANDA INSTT OF TECH AND SCI  BOMMAKAL", "KARIMNAGAR"], 
               217: ["WESL","CSI WESLEY INST OF TECHNOLOGY AND SCIENCES", "SECUNDERABAD"], 
               218: ["WITS","WARANGAL INST OF TECHNOLOGY SCIENCE", "WARANGAL"]}
            
               
               #5: [5108, "Nashik District Maratha Vidya Prasarak Samaj's Karmaveer Adv.Babaurao Ganpatrao Thakare College of Engineering, Nashik", "Nashik"]  }

    cet = int(request.GET.get('rank'))
    hsc = float(request.GET.get('percentage'))
    fee = request.GET.get('fee')
    caste = request.GET.get('caste')
    region = request.GET.get('region')
    branch = request.GET.get('branch')
    gender = request.GET.get('gender')
    
    gset=[0.0,0.0]
    cset=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    rset=[0.0,0.0,0.0,0.0]
    bset=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

    if hsc<50:
        messages.info(request, "HSC percentage need to above 50%")
        return render(request, 'home.html')
    else:
        
        if gender=='male':
            gset[0]=1.0
        else:
            gset[1]=1.0

        if caste=='oc':
            cset[0]=1.0
        elif caste=='bc_b':
            cset[1]=1.0
        elif caste=='bc_d':
            cset[2]=1.0
        elif caste=='sc':
            cset[3]=1.0
        elif caste=='st':
            cset[4]=1.0
        elif caste=='bc_e':
            cset[5]=1.0
        elif caste=='bc_a':
            cset[6]=1.0
        else:
            cset[7]=1.0
        
        if region=='ou':
            rset[0]=1.0
        elif region=='au':
            rset[1]=1.0
        elif region=='svu':
            rset[2]=1.0
        else:
            rset[3]=1.0

        #need to do
        if branch=='CSE':
            bset[0]=1.0
        elif branch=='ECE':
            bset[1]=1.0
        elif branch=='INF':
            bset[2]=1.0
        elif branch=='EEE':
            bset[3]=1.0
        elif branch=='CIV':
            bset[4]=1.0
        elif branch=='CSM':
            bset[5]=1.0
        elif branch=='MEC':
            bset[6]=1.0
        elif branch=='CSD':
            bset[7]=1.0
        elif branch=='CSC':
            bset[8]=1.0
        elif branch=='CSO':
            bset[9]=1.0
        elif branch=='CSI':
            bset[10]=1.0
        elif branch=='CHE':
            bset[11]=1.0
        elif branch=='CSB':
            bset[12]=1.0
        elif branch=='ANE':
            bset[13]=1.0
        elif branch=='EIE':
            bset[14]=1.0
        elif branch=='ECM':
            bset[15]=1.0
        elif branch=='AID':
            bset[16]=1.0
        elif branch=='MIN':
            bset[17]=1.0
        elif branch=='PHM':
            bset[18]=1.0
        elif branch=='AI':
            bset[19]=1.0
        elif branch=='AUT':
            bset[20]=1.0
        elif branch=='CSN':
            bset[21]=1.0
        elif branch=='MET':
            bset[22]=1.0
        elif branch=='DTD':
            bset[23]=1.0
        elif branch=='CIC':
            bset[24]=1.0
        elif branch=='BME':
            bset[25]=1.0
        elif branch=='ECI':
            bset[26]=1.0
        elif branch=='CME':
            bset[27]=1.0
        elif branch=='ETM':
            bset[28]=1.0
        elif branch=='ITE':
            bset[29]=1.0
        elif branch=='MCT':
            bset[30]=1.0
        elif branch=='CST':
            bset[31]=1.0
        elif branch=='PLG':
            bset[32]=1.0
        elif branch=='MMT':
            bset[33]=1.0
        elif branch=='CSW':
            bset[34]=1.0
        elif branch=='PHD':
            bset[35]=1.0
        elif branch=='MTE':
            bset[36]=1.0
        elif branch=='MMS':
            bset[37]=1.0
        elif branch=='TEX':
            bset[38]=1.0
        elif branch=='FPT':
            bset[39]=1.0
        elif branch=='FSP':
            bset[40]=1.0
        elif branch=='FDS':
            bset[41]=1.0
        elif branch=='AGR':
            bset[42]=1.0
        elif branch=='PHE':
            bset[43]=1.0
        elif branch=='DRG':
            bset[44]=1.0
        elif branch=='BIO':
            bset[45]=1.0
        elif branch=='IPE':
            bset[46]=1.0

        #print(cet)
        #cet=cet-2000
        if(cet>10000):
            cet-=10000
            ran=cet+(10000*3)
        else:
            cet-=1000
            ran=cet+(1000*3)

        list_college=[]
        string=""
        info=set()
        for i in range(cet,ran):
            details = gset + cset + rset + bset
            details.append(i)
            details.append(fee)
            ypred = model.predict([details])
            pred = college[ypred[0]]
            #print(pred)
            if pred[0] not in info:
                list_college.append([pred[0],pred[1],pred[2]])
                info.add(pred[0])
        #print(list_college)
        # for i in range(len(list_college)):
        #     string+=list_college[i][0]+','+list_college[i][1]+','+list_college[i][2]+'\n'

        # print(string)
        return render(request, 'result.html', {'answer':list_college})

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')
