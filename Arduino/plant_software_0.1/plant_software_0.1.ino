#include <EEPROM.h>

char id[6] = "defau";
int state = 0;

char[] loadId()
{
  // Read the ID from the EEPROM if flag is set.
  bool idIsSet;
  EEPROM.get(420, idIsSet);
  if (idIsSet)
  {
    Serial.println("Reading EEPROM");
    //EEPROM.get(0, id);
    for (int i = 0; i < 5; i++) {
      id[i] = EEPROM.read(i);
    }
    return id;
  }
  else
  {
    // Generate new ID
    for (int i = 0; i < 5; i++)
    {
      id[i] = random(97, 122);
    }

    // Save ID in EEPROM
    Serial.println("Writing EEPROM");
    EEPROM.put(0, id);

    Serial.println("Setting EEPROM flag");
    EEPROM.write(420, true);
  }



}

void setup()
{

  Serial.begin(9600);
  while (!Serial);
  Serial.println(" <-- GARBO BOARD");
  id = loadId();
  for (int i = 0; i < 7; i++)
  {
    Serial.print(id[i]);
  }
  Serial.println(".");
}

void loop()
{
  // Switch on state.
  switch (state)
  {
    case 0:
      // statements
      break;
    case 1:
      // statements
      break;
    default:
      // statements
      break;
  }
}




// EERPOM MEMORY ADDRESSES
// 0: ID SET FLAG
// 1-5: ID
