/*
	Copyright (C) 2011-2017 DeSmuME team

	This file is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 2 of the License, or
	(at your option) any later version.

	This file is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with the this software.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <time.h>


#include "advanscene.h"
#include "../common.h"
#include "../mc.h"
#include "../emufile.h"

#define SKIP_STDIO_REDEFINES
#include "streams/file_stream_transforms.h"

ADVANsCEne advsc;

#define _ADVANsCEne_BASE_ID "DeSmuME database (ADVANsCEne)\0x1A"
#define _ADVANsCEne_BASE_VERSION_MAJOR 1
#define _ADVANsCEne_BASE_VERSION_MINOR 0
#define _ADVANsCEne_BASE_NAME "ADVANsCEne Nintendo DS Collection"

u8 ADVANsCEne::checkDB(const char *ROMserial, u32 crc)
{
	loaded = false;
	RFILE *fp = rfopen(database_path.c_str(), "rb");
	if (fp)
	{
		char buf[64];
		memset(buf, 0, sizeof(buf));
		if (rfread(buf, 1, strlen(_ADVANsCEne_BASE_ID), fp) == strlen(_ADVANsCEne_BASE_ID))
		{
			//printf("ID: %s\n", buf);
			if (strcmp(buf, _ADVANsCEne_BASE_ID) == 0)
			{
				if (rfread(&versionBase[0], 1, 2, fp) == 2)
				{
					//printf("Version base: %i.%i\n", versionBase[0], versionBase[1]);
					if (rfread(&version[0], 1, 4, fp) == 4)
					{
						//printf("Version: %c%c%c%c\n", version[3], version[2], version[1], version[0]);
						if (rfread(&createTime, 1, sizeof(time_t), fp) == sizeof(time_t))
						{
							memset(buf, 0,sizeof(buf));
							// serial(8) + crc32(4) + save_type(1) = 13 + reserved(8) = 21
							while (true)
							{
								if (rfread(buf, 1, 21, fp) != 21) break;

								bool serialFound = (memcmp(&buf[4], ROMserial, 4) == 0);
								u32 dbcrc = LE_TO_LOCAL_32(*(u32*)(buf+8));
								bool crcFound = (crc == dbcrc);

								if(serialFound || crcFound)
								{
									foundAsCrc = crcFound;
									foundAsSerial = serialFound;
									memcpy(&crc32, &buf[8], 4);
									memcpy(&serial[0], &buf[4], 4);
									//printf("%s founded: crc32=%04X, save type %02X\n", ROMserial, crc32, buf[12]);
									saveType = buf[12];
									rfclose(fp);
									loaded = true;
									return true;
								}
							}
						}
					}
				}
			}
		}
		rfclose(fp);
	}
	return false;
}

 
void ADVANsCEne::setDatabase(const char *path)
{
	database_path = path;
	
	//i guess this means it needs (re)loading on account of the path having changed
	loaded = false;
}
