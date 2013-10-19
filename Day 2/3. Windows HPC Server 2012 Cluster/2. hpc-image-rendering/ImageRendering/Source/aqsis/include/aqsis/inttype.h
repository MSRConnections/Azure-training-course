// ----------------------------------------------------------------------------------
// Microsoft Developer & Platform Evangelism
// 
// Copyright (c) Microsoft Corporation. All rights reserved.
// 
// THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, 
// EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES 
// OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
// ----------------------------------------------------------------------------------
// The example companies, organizations, products, domain names,
// e-mail addresses, logos, people, places, and events depicted
// herein are fictitious.  No association with any real company,
// organization, product, domain name, email address, logo, person,
// places, or events is intended or should be inferred.
// ----------------------------------------------------------------------------------

/* Aqsis
 / Copyright (C) 1997 - 2001, Paul C. Gregory
 /
 / Contact: pgregory@aqsis.org
 /
 / This library is free software; you can redistribute it and/or
 / modify it under the terms of the GNU General Public
 / License as published by the Free Software Foundation; either
 / version 2 of the License, or (at your option) any later version.
 /
 / This library is distributed in the hope that it will be useful,
 / but WITHOUT ANY WARRANTY; without even the implied warranty of
 / MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 / General Public License for more details.
 /
 / You should have received a copy of the GNU General Public
 / License along with this library; if not, write to the Free Software
 / Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/


/** \file
 * \brief Declares typedefs for the basic types.
 * \author Paul C. Gregory (pgregory@aqsis.org)
 * \author Chris Foster (chris42f (at) gmail (d0t) com)
 *
 * ===================================================================
 * C-compatible header. C++ constructs must be preprocessor-protected.
 * ===================================================================
 */


#ifndef AQSIS_TYPES_INCLUDED
#define AQSIS_TYPES_INCLUDED

#include <aqsis/config.h>

/** \todo <b>Code review</b> Consider whether we can avoid polluting the global namespace with these typedefs.  C compatibility needs to be assured, so we may have to duplicate the header...
 */
/*--------------------------------------------------------------------------------*/
typedef char TqChar;
typedef unsigned char TqUchar;

/** \todo <b>Code review</b> Deprecate these pointer types?  They're inconsistently used and of dubious usefulness anyway.
 */
typedef char* TqPchar;
typedef unsigned char* TqPuchar;

typedef int TqInt;
typedef unsigned int TqUint;
typedef long TqLong;
typedef unsigned long TqUlong;

typedef short TqShort;
typedef unsigned short TqUshort;

typedef float TqFloat;
typedef double TqDouble;


/*--------------------------------------------------------------------------------
 / Typedefs for integer types with specific sizes.
 /
 / This approach - based on a combination of stdint.h and limit macros from
 / limits.h - is taken from boost/cstdint.hpp.  Unfortunately we have to use
 / our own version here for C compatibility.
*/

#ifdef AQSIS_HAVE_STDINT_H

	/* Use types from the C99 stdint.h header. */
#	include <stdint.h>

	typedef int8_t  TqInt8;
	typedef uint8_t TqUint8;

	typedef int16_t  TqInt16;
	typedef uint16_t TqUint16;

	typedef int32_t  TqInt32;
	typedef uint32_t TqUint32;

#else 

	/* If the stdint.h header is not present, fall back on using the limits
	  macros from limits.h to guess the correct types.
	*/
#	include <limits.h>

#	if UCHAR_MAX == 0xff
		typedef signed char   TqInt8;
		typedef unsigned char TqUint8;
#	else
#		error 8 bit integers not autodetected - please modify aqsis_types.h \
			or contact the aqsis team.
#	endif

#	if USHRT_MAX == 0xffff
		typedef short          TqInt16;
		typedef unsigned short TqUint16;
#	else
#		error 16 bit integers not autodetected - please modify aqsis_types.h \
			or contact the aqsis team.
#	endif

#	if ULONG_MAX == 0xffffffff
		typedef long          TqInt32;
		typedef unsigned long TqUint32;
#	elif UINT_MAX == 0xffffffff
		typedef int           TqInt32;
		typedef unsigned int  TqUint32;
#	else
#		error 32 bit integers not autodetected - please modify aqsis_types.h \
			or contact the aqsis team.
#	endif

#endif 


#endif 
