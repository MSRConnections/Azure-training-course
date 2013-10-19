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
 * Copyright (C) 1997 - 2001, Paul C. Gregory
 *
 * Contact: pgregory@aqsis.org
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

/** \file
 * \brief RI filters interface
 *
 * Define the RenderMan Interface filters API
 *
 * ===================================================================
 * C-compatible header. C++ constructs must be preprocessor-protected.
 * ===================================================================
 */

#ifndef RIF_H_INCLUDED
#define RIF_H_INCLUDED

#include <aqsis/config.h>
#include <aqsis/ri/ritypes.h>

/** \brief Primitive variable type identifiers */
typedef enum
{
	k_RifFloat=0,
	k_RifPoint,
	k_RifColor,
	k_RifInteger,
	k_RifString,
	k_RifVector,
	k_RifNormal,
	k_RifHPoint,
	k_RifMatrix,
	k_RifMPoint
} RifTokenType;

/** \brief Primitive variable interpolation classes */
typedef enum
{
	k_RifConstant=0,
	k_RifUniform,
	k_RifVarying,
	k_RifVertex,
	k_RifFaceVarying,
	k_RifFaceVertex
} RifTokenDetail;

#ifdef  __cplusplus
extern "C" {
#endif

/** \brief Look up a RI token in the internal dictionary.
 *
 * This function looks up previously declared tokens (those which have been
 * declared via RiDeclare()), and returns the type, interpolation class and
 * array length.  It can also parse inline declarations.
 *
 * \param name - name of the token, or inline declaration
 *
 * \param tokType -   type for values associated with the token 
 * \param tokDetail - interpolation class
 * \param arrayLen -  array length; for non-array tokens 1 is returned since
 *                    the amount of storage is the same for a non-array and for
 *                    a length-1 array.
 *
 * \return 0 on success in which case tokType, tokClass and arrayLen are set to
 * appropriate values.  1 is returned if the function was unable to parse the
 * token or find the token name in the internal dictionary.
 */
AQSIS_RI_SHARE RtInt RifGetDeclaration(RtToken name, RifTokenType *tokType,
		RifTokenDetail *tokDetail, RtInt *arrayLen);

#ifdef  __cplusplus
}
#endif

#endif /* RIF_H_INCLUDED */
