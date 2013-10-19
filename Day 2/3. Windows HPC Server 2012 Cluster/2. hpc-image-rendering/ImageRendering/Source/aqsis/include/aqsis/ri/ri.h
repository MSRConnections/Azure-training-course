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

/*----------------------------------------------------------------------------*/
/** \file
 * \brief Aqsis implementation of the Renderman Interface version 3.2
 *
 * The Renderman Interface is Copyright (c) 1988 Pixar. All Rights reserved.
 *
 * ===================================================================
 * C-compatible header. C++ constructs must be preprocessor-protected.
 * ===================================================================
 */
/*----------------------------------------------------------------------------*/

#ifndef RI_H_INCLUDED
#define RI_H_INCLUDED

#include <aqsis/config.h>

#include <float.h>

#include <aqsis/ri/ritypes.h>

#ifdef	__cplusplus
extern	"C"
{
#endif

	/*
	 *		RenderMan Interface Standard Include File
	 */

#define	RI_FALSE	0
#define	RI_TRUE		1
#define	RI_INFINITY	FLT_MAX
#define	RI_EPSILON	FLT_EPSILON
#define	RI_NULL		((RtToken)0)

#define	RI_FLOATMIN	FLT_MIN
#define	RI_FLOATMAX	FLT_MAX

#define	RI_PI		3.14159265359f
#define	RI_PIO2		RI_PI/2

#define	RI_SHADER_EXTENSION	".slx"

	/* Extern Declarations for Predefined RI Data Structures */

	AQSIS_RI_SHARE	extern	RtToken	RI_FRAMEBUFFER, RI_FILE;
	AQSIS_RI_SHARE	extern	RtToken	RI_RGB, RI_RGBA, RI_RGBZ, RI_RGBAZ, RI_A, RI_Z, RI_AZ;
	AQSIS_RI_SHARE	extern	RtToken	RI_MERGE, RI_ORIGIN;
	AQSIS_RI_SHARE	extern	RtToken	RI_PERSPECTIVE, RI_ORTHOGRAPHIC;
	AQSIS_RI_SHARE	extern	RtToken	RI_HIDDEN, RI_PAINT;
	AQSIS_RI_SHARE	extern	RtToken	RI_CONSTANT, RI_SMOOTH;
	AQSIS_RI_SHARE	extern	RtToken	RI_FLATNESS, RI_FOV;

	AQSIS_RI_SHARE	extern	RtToken	RI_AMBIENTLIGHT, RI_POINTLIGHT,
	RI_DISTANTLIGHT, RI_SPOTLIGHT;
	AQSIS_RI_SHARE	extern	RtToken	RI_INTENSITY, RI_LIGHTCOLOR, RI_FROM, RI_TO,
	RI_CONEANGLE, RI_CONEDELTAANGLE,
	RI_BEAMDISTRIBUTION;
	AQSIS_RI_SHARE	extern	RtToken	RI_MATTE, RI_METAL, RI_PLASTIC, RI_SHINYMETAL, RI_PAINTEDPLASTIC;
	AQSIS_RI_SHARE	extern	RtToken	RI_KA, RI_KD, RI_KS, RI_ROUGHNESS, RI_KR,
	RI_TEXTURENAME, RI_SPECULARCOLOR;
	AQSIS_RI_SHARE	extern	RtToken	RI_DEPTHCUE, RI_FOG, RI_BUMPY;
	AQSIS_RI_SHARE	extern	RtToken	RI_MINDISTANCE, RI_MAXDISTANCE, RI_BACKGROUND,
	RI_DISTANCE, RI_AMPLITUDE;

	AQSIS_RI_SHARE	extern	RtToken	RI_RASTER, RI_SCREEN, RI_CAMERA, RI_WORLD,
	RI_OBJECT;
	AQSIS_RI_SHARE	extern	RtToken	RI_INSIDE, RI_OUTSIDE, RI_LH, RI_RH;
	AQSIS_RI_SHARE	extern	RtToken	RI_P, RI_PZ, RI_PW, RI_N, RI_NP, RI_CS, RI_OS,
	RI_S, RI_T, RI_ST;
	AQSIS_RI_SHARE	extern	RtToken	RI_BILINEAR, RI_BICUBIC;
	AQSIS_RI_SHARE	extern	RtToken	RI_LINEAR, RI_CUBIC;
	AQSIS_RI_SHARE	extern	RtToken	RI_PRIMITIVE, RI_INTERSECTION, RI_UNION,
	RI_DIFFERENCE;
	AQSIS_RI_SHARE	extern	RtToken	RI_WRAP, RI_NOWRAP, RI_PERIODIC, RI_NONPERIODIC, RI_CLAMP,
	RI_BLACK;
	AQSIS_RI_SHARE	extern	RtToken	RI_IGNORE, RI_PRINT, RI_ABORT, RI_HANDLER;
	AQSIS_RI_SHARE	extern	RtToken	RI_IDENTIFIER, RI_NAME;
	AQSIS_RI_SHARE	extern	RtToken	RI_COMMENT, RI_STRUCTURE, RI_VERBATIM;
	AQSIS_RI_SHARE	extern	RtToken	RI_WIDTH, RI_CONSTANTWIDTH;

	AQSIS_RI_SHARE	extern	RtToken	RI_CURRENT, RI_SHADER, RI_EYE, RI_NDC;

	AQSIS_RI_SHARE	extern	RtBasis	RiBezierBasis, RiBSplineBasis, RiCatmullRomBasis,
	RiHermiteBasis, RiPowerBasis;

// Spline basis steps
#define	RI_BEZIERSTEP		((RtInt)3)
#define	RI_BSPLINESTEP		((RtInt)1)
#define	RI_CATMULLROMSTEP	((RtInt)1)
#define	RI_HERMITESTEP		((RtInt)2)
#define	RI_POWERSTEP		((RtInt)4)

// Aqsis-specific "matte with alpha" argument to RiMatte.
#define RI_MATTEALPHA 2

	AQSIS_RI_SHARE	extern	RtInt	RiLastError;

	/* Declarations of All of the RenderMan Interface Subroutines */

#define	PARAMETERLIST	RtInt count, RtToken tokens[], RtPointer values[]

	/* Include the automatically generated procedure declarations. 
	   Generated from api.xml, using apiheader.xsl */

#include	"aqsis/ri/ri.inl"

	/* Specific to Aqsis */

	AQSIS_RI_SHARE	RtBoolean	BasisFromName( RtBasis * b, const char * strName );
	AQSIS_RI_SHARE	RtVoid	RiProgressHandler( RtProgressFunc handler );
	AQSIS_RI_SHARE	RtFunc	RiPreRenderFunction( RtFunc function );
	AQSIS_RI_SHARE	RtFunc	RiPreWorldFunction( RtFunc function );

#ifdef	__cplusplus
}
#endif

/*
  Error Codes
  
   1 - 10         System and File Errors
  11 - 20         Program Limitations
  21 - 40         State Errors
  41 - 60         Parameter and Protocol Errors
  61 - 80         Execution Errors
*/
#define RIE_NOERROR     ((RtInt)0)

#define RIE_NOMEM       ((RtInt)1)      /* Out of memory */
#define RIE_SYSTEM      ((RtInt)2)      /* Miscellaneous system error */
#define RIE_NOFILE      ((RtInt)3)      /* File nonexistent */
#define RIE_BADFILE     ((RtInt)4)      /* Bad file format */
#define RIE_VERSION     ((RtInt)5)      /* File version mismatch */
#define RIE_DISKFULL    ((RtInt)6)      /* Target disk is full */

#define RIE_INCAPABLE   ((RtInt)11)     /* Optional RI feature */
#define RIE_UNIMPLEMENT ((RtInt)12)     /* Unimplemented feature */
#define RIE_LIMIT       ((RtInt)13)     /* Arbitrary program limit */
#define RIE_BUG         ((RtInt)14)     /* Probably a bug in renderer */

#define RIE_NOTSTARTED  ((RtInt)23)     /* RiBegin not called */
#define RIE_NESTING     ((RtInt)24)     /* Bad begin-end nesting */
#define RIE_NOTOPTIONS  ((RtInt)25)     /* Invalid state for options */
#define RIE_NOTATTRIBS  ((RtInt)26)     /* Invalid state for attribs */
#define RIE_NOTPRIMS    ((RtInt)27)     /* Invalid state for primitives */
#define RIE_ILLSTATE    ((RtInt)28)     /* Other invalid state */
#define RIE_BADMOTION   ((RtInt)29)     /* Badly formed motion block */
#define RIE_BADSOLID    ((RtInt)30)     /* Badly formed solid block */

#define RIE_BADTOKEN    ((RtInt)41)     /* Invalid token for request */
#define RIE_RANGE       ((RtInt)42)     /* Parameter out of range */
#define RIE_CONSISTENCY ((RtInt)43)     /* Parameters inconsistent */
#define RIE_BADHANDLE   ((RtInt)44)     /* Bad object/light handle */
#define RIE_NOSHADER    ((RtInt)45)     /* Can't load requested shader */
#define RIE_MISSINGDATA ((RtInt)46)     /* Required parameters not provided */
#define RIE_SYNTAX      ((RtInt)47)     /* Declare type syntax error */

#define RIE_MATH        ((RtInt)61)     /* Zerodivide, noninvert matrix, etc. */

/* Error severity levels */
#define RIE_INFO        ((RtInt)0)      /* Rendering stats and other info */
#define RIE_WARNING     ((RtInt)1)      /* Something seems wrong, maybe okay */
#define RIE_ERROR       ((RtInt)2)      /* Problem. Results may be wrong */
#define RIE_SEVERE      ((RtInt)3)      /* So bad you should probably abort */


#endif 
