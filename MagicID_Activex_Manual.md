# MagicID ActiveX User Manual

MinervaSoft

작성일 : 2021.07.15

---

## 목차 

  [1.개발환경](#1개발환경)

  [2.라이브러리 구성](#2라이브러리-구성)

  [3.인터페이스 리스트](#3인터페이스-리스트)

  [4.인터페이스 상세설명](#4인터페이스-상세설명)
  
  [5.사용예제](#5사용예제)

  [6.기타](#6기타)



---

## 1.개발환경

|항목     |사양|
|--------|----|
|OS      | Windows 10|
|개발언어 | Visual C++(vs2017) |

---

## 2. ActiveX 구성

### GUID

 8506A17B-4637-4269-92EE-A89C5D7CAEDF 

### 필수 파일
    반드시 Data파일이 MagicIDX.ocx가 위치한 동일 폴더에 위치해야 하며 
    아래 참조 라이브러리 (DLL) 파일이 설치 폴더내에 위치 해야한다.

 1. **_참조 Library_**
   - MagicID.dll
   - Jsoncpp.dll 

 2. **_Data 폴더 파일 리스트_**

   - **Face**

     - haarcascade_frontalface_alt.xml

   - **ML**

     - IDCard_01.xml
     - IDCard_02.xml
     - IDCard_03.xml
     - IDCard_04.xml
     - IDCard_05.xml
     - IDCard_06.xml
     - IDCard_07.xml
     - IDCard_Date_Gullimche_SVM.xml
     - IDCard_Gender_Gullimche_SVM.xml
     - IDCard_Passport_MRZ1_Sign_Gullimche_SVM.xml
     - IDCard_Passport_Type_Gullimche_SVM.xml

   - eng.trainddata
   - jhangul.traineddata
   - kor.traineddata
   - ocrb.traineddata

### 등록 및 설치
  
  설치는 regsvr32를 command prompt에서 실행하여 ocx를 등록 할 수 있다.
  >c:\설치폴더\regsvr32 MagicIDX.ocx

  설치 및 실행시에는 MagicIDX.ocx가 위치한 폴더에 참조 Library와 data파일이 반드시 위치 해야 한다.
  <span style="color:red">인식 모듈은 Visual Studio 2017로 개발 되었으므로 재배포패키지 2015가 ocx 등록전에 반드시 설치되어 있어야 한다.</span>

---

## 3.인터페이스 리스트

| 번호 |  인터페이스 명                       |    기능                                                        |
|------|-------------------------------------|---------------------------------------------------------------|
| 1    | Process_KBInsulance |  신분증을 인식하고 전달 변수에 인식 값 저장              |
| 2    | Process_KBInsulance_IDMasking | 개인정보를 마스킹하기 위해 사용      |
| 3    | Process_KBInsulance_DrawingRect |  전체 인식 영역 사각형 표시     |
| 4    | Process_KBInsulance_DrawingSingleRect |  특정 인식 영역 사각형 표시     |
| 5    | Process_KBInsulance_Test |  전체 동작 테스트를 위해 사용    |

---

## 4.인터페이스 상세설명

  ## Process_KBInsulance


  #### [ 기능  ]
    
   입력받은 file path의 이미지를 인식하고 인식결과를 전달된 변수포인터에 저장한다.

  #### [ 원형 ] 

     void Process_KBInsulance(BSTR filePath, BSTR* type, 
                               BSTR* DLN, BSTR* idNum, BSTR* name, BSTR* date, BSTR* codeid, BSTR* gender, BSTR* country, 
                               BSTR* rtDLN, BSTR* rtIDNum, BSTR* rtName, BSTR* rtDate, BSTR* rt Code, BSTR* rtGender, BSTR* rtCountry) 

  #### [ Parameters ]

  |파라메터 명 | 파라메터 Type  | 설명
  |------------|--------------|-----------------------------------|
  | filePath   | BSTR         | 인식에 사용할 원본 파일의 절대 경로 |
  | type       | BSTR*        | 인식된 신분증 종류 저장 변수         |
  | DLN       | BSTR*        | 운전면허번호 저장 변수                |
  | idNum       | BSTR*        | 주민등록번호 저장 변수                |
  | Name       | BSTR*        | 이름 저장 변수                |
  | Date       | BSTR*        | 발행일자 저장 변수                |
  | codeid       | BSTR*        | 운전면허증 코드 저장 변수                |
  | gender      | BSTR*        | 성별 저장 변수                |
  | country      | BSTR*        | 국적 저장 변수                |
  | rtDLN      | BSTR*        | 운전면허번호 위치 텍스트 저장 변수|
  | rtIDNum      | BSTR*        | 주민증록번호 위치 텍스트 저장 변수|
  | rtName      | BSTR*        | 이름 위치 텍스트 저장 변수|
  | rtDate      | BSTR*        | 발행일자 위치 텍스트 저장 변수|
  | rtCode      | BSTR*        | 운전면허번호 코드 위치 텍스트 저장 변수|
  | rtGender      | BSTR*        | 성별 위치 텍스트 저장 변수|
  | rtCountry      | BSTR*        | 국적 위치 텍스트 저장 변수|

  #### [ Return ]
    (void) 리턴 값 없음

---
  ## Process_KBInsulance_IDMasking

  
  #### [ 기능 ]
   주민등록 번호와 같이 마스킹이 필요한 부분을 특정 색깔 사각형으로 마스킹해서 파일로 저장한다.

  #### [ 원형 ]
    void Process_KBInsulance_ID Masking( BSTR inFilePath, BSTR outFilePath, BSTR rtIDNum, BSTR color )

  #### [ Parameters ]

  |파라메터 명 | 파라메터 Type  | 설명
  |---------------|--------------|-----------------------------------|
  | inFilePath    | BSTR         | 인식에 사용할 원본 파일의 절대 경로  |
  | outFilePath   | BSTR         | 인식에 사용할 결과 파일의 절대 경로 |
  | rtIDNum       | BSTR         | 마스킹할 영역 **_예) 0,0,100,50_**       |
  | color         | BSTR         | 컬러 텍스트 **_예) Red_**                |

  #### [ Return ]
    (void) 리턴 값 없음

---
  ## Process_KBInsulance_DrawingRect

  #### [ 기능 ]
   파라메터로 입력된 영역들을 원본에 그린 후 파일로 출력한다. 

  #### [ 원형 ]
    void Process_KBInsulance_DrawingRect( BSTR inFilePath, BSTR outFilePath, BSTR rtDLN, BSTR rtIDNum, 
                                        BSTR rtName BSTR rtDate, BSTR rtCode, BSTR rtGender, 
                                        BSTR rtCountry, BSTR color, LONG thickness )

  #### [ Parameters ]

  |파라메터 명 | 파라메터 Type  | 설명
  |---------------|--------------|-----------------------------------|
  | inFilePath    | BSTR         | 인식에 사용할 원본 파일의 절대 경로  |
  | outFilePath   | BSTR         | 인식에 사용할 결과 파일의 절대 경로 |
  | rtDLN         | BSTR         | 운전면허번호 좌표 텍스트 **_예) 0,0,100,50_** |
  | rtIDNum       | BSTR         | 주민등록번호 영역좌표 텍스트       |
  | rtName       | BSTR         | 이름영역 좌표텍스트       |
  | rtDate       | BSTR         | 발행일 좌표 텍스트       |
  | rtCode       | BSTR         | 운전면허증 코드 좌표 텍스트       |
  | rtGender      | BSTR         | 성별 좌표 텍스트      |
  | rtCountry     | BSTR         | 국적 좌표 텍스트       |
  | color         | BSTR         | 컬러 텍스트 **_예) Red_**                |
  | thickness     | BSTR         | 선 두께 **_(입력범위 : 1 ~ 3)_**         |

  #### [ Return ]
    (void) 리턴 값 없음

---
  ## Process_KBInsulance_DrawingSingleRect

  #### [ 기능 ]
   파라메터로 입력된 하나의 영역을 원본에 그린 후 파일로 출력한다. 

  #### [ 원형 ]
    void Process_KBInsulance_DrawingSingleRect( BSTR inFilePath, BSTR outFilePath, BSTR rect 
                                                ,BSTR color, LONG thickness )

  #### [ Parameters ]

  |파라메터 명 | 파라메터 Type  | 설명
  |---------------|--------------|-----------------------------------|
  | inFilePath    | BSTR         | 인식에 사용할 원본 파일의 절대 경로  |
  | outFilePath   | BSTR         | 인식에 사용할 결과 파일의 절대 경로 |
  | rect         | BSTR         | 운전면허번호 좌표 텍스트 **_예) 0,0,100,50_** |
  | color         | BSTR         | 컬러 텍스트 **_예) Red_**               |
  | thickness     | BSTR         | 선 두께 **_(입력범위 : 1 ~ 3)_**         |

  #### [ Return ]
    (void) 리턴 값 없음
---
  ## Process_KBInsulance_Test

  #### [ 기능 ]
   단순 테스트용 인터페이스
   입력 파일명에 상관없이 동일한 결과를 변수에 저장한다.

  #### [ 원형 ]

     void Process_KBInsulance_Test (BSTR filePath, BSTR* type, 
                               BSTR* DLN, BSTR* idNum, BSTR* name, BSTR* date, BSTR* codeid, BSTR* gender, BSTR* country, 
                               BSTR* rtDLN, BSTR* rtIDNum, BSTR* rtName, BSTR* rtDate, BSTR* rt Code, BSTR* rtGender, BSTR* rtCountry) 

  #### [ Parameters ]

  |파라메터 명 | 파라메터 Type  | 설명
  |------------|--------------|-----------------------------------|
  | filePath   | BSTR         | 인식에 사용할 원본 파일의 절대 경로 |
  | type       | BSTR*        | 인식된 신분증 종류 저장 변수         |
  | DLN       | BSTR*        | 운전면허번호 저장 변수                |
  | idNum       | BSTR*        | 주민등록번호 저장 변수                |
  | Name       | BSTR*        | 이름 저장 변수                |
  | Date       | BSTR*        | 발행일자 저장 변수                |
  | codeid       | BSTR*        | 운전면허증 코드 저장 변수                |
  | gender      | BSTR*        | 성별 저장 변수                |
  | country      | BSTR*        | 국적 저장 변수                |
  | rtDLN      | BSTR*        | 운전면허번호 위치 텍스트 저장 변수|
  | rtIDNum      | BSTR*        | 주민증록번호 위치 텍스트 저장 변수|
  | rtName      | BSTR*        | 이름 위치 텍스트 저장 변수|
  | rtDate      | BSTR*        | 발행일자 위치 텍스트 저장 변수|
  | rtCode      | BSTR*        | 운전면허번호 코드 위치 텍스트 저장 변수|
  | rtGender      | BSTR*        | 성별 위치 텍스트 저장 변수|
  | rtCountry      | BSTR*        | 국적 위치 텍스트 저장 변수|

  #### [ Return ]
    (void) 리턴 값 없음

---

## 5.사용예제

### C#에서 사용 예

1. Form > Toolbox 에서 COM Components **MagicIDX Control**를 추가 한다.

2. Form에 MagicIDX Control ocx를 추가 한다.

3. Button 이벤트 또는 필요한 메소드에 아래와 같이 코드를 구현해서 MagicIDX를 이용할 수 있다.

_(상세 코드는 모듈과 같이 첨부된 Sample Application 소스코드 참조)_

**Code:**
~~~ csharp
private void ProcessImage_Click(object sender, EventArgs e)
        {
            string outText = "";

            string imagePath = "";
            //string fileName = @"D:\Works\Source\MagicIDWrapper\samples\jumin.tif";
            string maskingFileName = @"D:\Works\Source\MagicIDWrapper\samples\masking.png";
            string singleRectFileName = @"D:\Works\Source\MagicIDWrapper\samples\single_rect.png";
            string multiRectFileName = @"D:\Works\Source\MagicIDWrapper\samples\multi_rect.png";
            string type = "";

            string DLN = "";
            string idNum = "";
            string name = "";
            string date = "";
            string codeid = "";
            string gender = "";
            string country = "";

            string rtDLN = "";
            string rtIDNum = "";
            string rtName = "";
            string rtDate = "";
            string rtCode = "";
            string rtGender = "";
            string rtCountry = "";
            string maskingColor = "Gray";
            string rectColor = "Blue";

            int thickness = 2;

            string version = axIDCard1.Version();

            OpenFileDialog openDlg = new OpenFileDialog();
            openDlg.InitialDirectory = "D:\\Samples\\신분증\\신분증_스캔";
            openDlg.Filter = "All files(*.*)|*.*|Tif (*.tif)|*.tif";

            if (openDlg.ShowDialog() == DialogResult.OK)
            {
                imagePath = openDlg.FileName;

                textBox1.Text = "";

                axIDCard1.Process_KBInsulance(imagePath, ref type, ref DLN, ref idNum, ref name, ref date, ref codeid, ref gender, ref country, ref rtDLN, ref rtIDNum, ref rtName, ref rtDate, ref rtCode, ref rtGender, ref rtCountry);

                outText = imagePath;
                outText = outText + "\r\n" + type;
                outText = outText + "\r\n" + DLN;
                outText = outText + "\r\n" + idNum;
                outText = outText + "\r\n" + name;
                outText = outText + "\r\n" + date;
                outText = outText + "\r\n" + codeid;
                outText = outText + "\r\n" + gender;
                outText = outText + "\r\n" + country;

                textBox1.Text = outText;

                // 주민등록번호 마스킹 이미지
                axIDCard1.Process_KBInsulance_IDMasking(imagePath, maskingFileName, rtIDNum, maskingColor);

                // 영역 하나만 그림
                axIDCard1.Process_KBInsulance_DrawingSingleRect(imagePath, singleRectFileName, rtName, rectColor, thickness);

                // 전체 영역을 그림
                axIDCard1.Process_KBInsulance_DrawingRect(imagePath, multiRectFileName, rtDLN, rtIDNum, rtName, rtDate, rtCode, rtGender, rtCountry, rectColor, thickness);

            }

        }
        
~~~
---

## 6.기타


---

