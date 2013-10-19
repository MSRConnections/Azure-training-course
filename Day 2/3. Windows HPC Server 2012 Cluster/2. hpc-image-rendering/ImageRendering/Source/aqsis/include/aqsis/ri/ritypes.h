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
 * \brief Definitions of types used by the RenderMan Interface
 *
 * ===================================================================
 * C-compatible header. C++ constructs must be preprocessor-protected.
 * ===================================================================
 */

#ifndef RI_TYPES_H_INCLUDED
#define RI_TYPES_H_INCLUDED

#ifdef __cplusplus
extern	"C"
{
#endif

typedef	short	RtBoolean;
typedef	int		RtInt;
typedef	float	RtFloat;

typedef	char*	RtToken;

typedef	RtFloat	RtColor[ 3 ];
typedef	RtFloat	RtPoint[ 3 ];
typedef RtFloat RtVector[ 3 ];
typedef RtFloat RtNormal[ 3 ];
typedef RtFloat RtHpoint[ 4 ];
typedef	RtFloat	RtMatrix[ 4 ][ 4 ];
typedef	RtFloat	RtBasis[ 4 ][ 4 ];
typedef	RtFloat	RtBound[ 6 ];
typedef	char*	RtString;

typedef	void*	RtPointer;
typedef	void	RtVoid;

typedef	RtFloat	( *RtFilterFunc ) ( RtFloat, RtFloat, RtFloat, RtFloat );
typedef	RtFloat	( *RtFloatFunc ) ();
typedef	RtVoid	( *RtFunc ) ();
typedef	RtVoid	( *RtErrorFunc ) ( RtInt code, RtInt severity, RtString message );
typedef	RtErrorFunc	RtErrorHandler;

typedef	RtVoid	( *RtProcSubdivFunc ) ( RtPointer, RtFloat );
typedef	RtVoid	( *RtProcFreeFunc ) ( RtPointer );
typedef	RtVoid	( *RtArchiveCallback ) ( RtToken, char *, ... );

typedef	RtPointer	RtObjectHandle;
typedef	RtPointer	RtLightHandle;
typedef	RtPointer	RtContextHandle;


/* Aqsis-specific typedefs */
typedef	RtVoid	( *RtProgressFunc ) ( RtFloat PercentComplete, RtInt FrameNo );

#ifdef	__cplusplus

/** tokenCast
 * /brief The RISpec prevents us from doing The Right Thing (tm) and using:
 *
 *   typedef const char* RtToken;
 *
 * The RISpec clearly specifies:
 * 
 *   typedef char* RtToken;
 *
 * Whereas using const char* would have made much more sense.  At the same time, there's
 * probably lots of code which relies on RtToken being non-const, so we can't just modify
 * the typedef.
 * 
 * Please use this convience function to avoid the conversion warning when using a RtToken
 *   warning: deprecated conversion from string constant to 'char*'
 **/
inline char* tokenCast(const char* token)
{
	return const_cast< char* >(token);
}

}
#endif

#endif 
