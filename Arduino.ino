#include <SPI.h>
#include<MFRC522.h>

#define SS_PIN 10 
#define RST_PIN 9
#define cards 1

MFRC522 rfid(SS_PIN,RST_PIN);
MFRC522::MIFARE_Key key; 
byte db_tag[cards][4]={{249,176,12,153}};
byte tag_data[3][3];
int i, j=0;

void setup() 
{
  Serial.begin(9600);

  SPI.begin();    // Initialize serial communication.
  rfid.PCD_Init();      // Initialize MFRC522 chip.
  for(i=0;i<6;i++)
  {
    key.keyByte[i]=0xFF;      // All keys are set to FFFFFFFFFFFFh from the factory. 
  }
}

// Infinite Loop
void loop()
{
  int s=0;
  if(!rfid.PICC_IsNewCardPresent())     // Look for new cards.
  return;
  if(!rfid.PICC_ReadCardSerial())       // Read the card.
  return;
  for(i=0;i<4;i++)
  {
    tag_data[0][i]=rfid.uid.uidByte[i]; 
    delay(50);
  }
  
  for(i=0;i<cards;i++)
  {
    if(db_tag[i][0]==tag_data[0][0])          // Checking if the tag is valid.
    {
      if(db_tag[i][1]==tag_data[0][1])
      {
        if(db_tag[i][2]==tag_data[0][2])
        {
          if(db_tag[i][3]==tag_data[0][3])
          {
            Serial.println(" ");
            for(s=0;s<4;s++)
            {
              Serial.print(rfid.uid.uidByte[s]);
            }
            Serial.print("  valid");
                  
            j=0;
            rfid.PICC_HaltA();          // Instructs a PICC in state Active to go to state HALT.
            rfid.PCD_StopCrypto1();     // Used to exit the PCD from its authenticated state.
            return; 
          }
        }
      }
    }
    else
    {
      j++;
      if(j==cards)
      {
        Serial.println(" ");
        for(s=0;s<4;s++)
        {
          Serial.print(rfid.uid.uidByte[s]);
        }
        Serial.print("  invalid");
        j=0;
      }
    }
  }
  rfid.PICC_HaltA();          // Instructs a PICC in state Active to go to state HALT.
  rfid.PCD_StopCrypto1();     // Used to exit the PCD from its authenticated state.
}