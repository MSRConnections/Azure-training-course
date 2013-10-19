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

//------------------------------------------------------------------------------
// Menger Sponge primitive as renderman ProcDynamicLoad procedural geometry.
//
// Copyright (C) 2008 Chris Foster
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public
// License as published by the Free Software Foundation; either
// version 2 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
//
// Author: Chris Foster [chris42f (at) gmail (d0t) com]
//

#include <ri.h>

#include <sstream>
#include <iostream>
//#include <cstdlib>

extern "C" AQSIS_EXPORT RtPointer ConvertParameters(char* initialdata);
extern "C" AQSIS_EXPORT void Subdivide(RtPointer blinddata, RtFloat detailsize);
extern "C" AQSIS_EXPORT void Free(RtPointer blinddata);


/** A simple vector class with overloaded operators
 */
struct Vec3
{
	RtFloat x;
	RtFloat y;
	RtFloat z;

	Vec3(RtFloat x, RtFloat y, RtFloat z) : x(x), y(y), z(z) {}
	Vec3(RtFloat a) : x(a), y(a), z(a) {}

	Vec3 operator+(const Vec3& rhs) const { return Vec3(x + rhs.x, y + rhs.y, z + rhs.z); }
	Vec3 operator-(const Vec3& rhs) const { return Vec3(x - rhs.x, y - rhs.y, z - rhs.z); }
	Vec3 operator*(float a) const { return Vec3(a*x, a*y, a*z); }
};

Vec3 operator*(float a, const Vec3& v) { return v*a; }


/** Draw an axis-aligned cube, defined by the the minimum and maximum
 * coordinates of the corners.
 */
void drawCube(Vec3 min, Vec3 max)
{
	RtInt nverts[] = {4, 4, 4, 4, 4, 4};
	RtInt verts[] = {
		0, 1, 2, 3, 
		4, 7, 6, 5, 
		0, 4, 5, 1,
		3, 2, 6, 7, 
		1, 5, 6, 2, 
		0, 3, 7, 4
	};
	RtFloat P[] = {
		min.x, min.y, min.z,
		max.x, min.y, min.z,
		max.x, min.y, max.z,
		min.x, min.y, max.z,
		min.x, max.y, min.z,
		max.x, max.y, min.z,
		max.x, max.y, max.z,
		min.x, max.y, max.z
	};

	RiPointsPolygons(6, nverts, verts, "P", P, RI_NULL);
}


/** Class representing a menger sponge fractal, capable of recursively
 * subdividing itself.
 */
class MengerSponge
{
	private:
		// Level to which this sponge should be subdivided.  0 == no subdivision.
		int m_level;
		// minimum of axis-aligned box bounding the sponge
		Vec3 m_min;
		// maximum of axis-aligned box bounding the sponge
		Vec3 m_max;

	public:
		MengerSponge(int level, const Vec3& min, const Vec3& max)
			: m_level(level),
			m_min(min),
			m_max(max)
		{ }
		/** Extract sponge parameters from a string
		 *
		 * initString is in the form "level  x1 x2  y1 y1  z2 z2"
		 */
		MengerSponge(const char* initString)
			: m_level(1),
			m_min(-1),
			m_max(1)
		{
			std::istringstream(initString) >> m_level
				>> m_min.x >> m_max.x
				>> m_min.y >> m_max.y
				>> m_min.z >> m_max.z;
		}

		/** Fill a renderman bound array with the bound for the current
		 * primitive.
		 */
		void bound(RtBound bnd) const
		{
			bnd[0] = m_min.x;
			bnd[1] = m_max.x;
			bnd[2] = m_min.y;
			bnd[3] = m_max.y;
			bnd[4] = m_min.z;
			bnd[5] = m_max.z;
		}

		/** Create a child of the current sponge
		 *
		 * xOff, yOff and zOff are the integer coordinates of the child within
		 * an even 3x3x3 subdivision of the current bounding box.  RiProcedural()
		 * is called recursively to add the subdivided child primitives to the
		 * render pipeline.
		 */
		void createChild(int xOff, int yOff, int zOff) const
		{
			RtBound bnd;
			Vec3 diag = (1/3.0)*(m_max - m_min);
			Vec3 newMin = m_min + Vec3(xOff*diag.x, yOff*diag.y, zOff*diag.z);
			MengerSponge* pNew = new MengerSponge(m_level-1, newMin, newMin + diag);
			pNew->bound(bnd);
			RiProcedural(pNew, bnd, Subdivide, Free);
		}

		/** Split the procedural up according to the fractal subdivision rules.
		 *
		 * We iterate through all of the set of 3x3x3 sub-cubes, deciding which
		 * ones to draw based on the fractal recursion relation.  Each drawn
		 * subcube is subdivided in the same way until leaf nodes of the
		 * subdivision tree are reached.
		 */
		void subdivide() const
		{
			if(m_level <= 0) // || m_level/4.0 < std::rand()/float(RAND_MAX))
				drawCube(m_min, m_max);
			else
			{
				for(int zOff = 0; zOff < 3; ++zOff)
				{
					for(int yOff = 0; yOff < 3; ++yOff)
					{
						for(int xOff = 0; xOff < 3; ++xOff)
						{
							//if(xOff == 1 || yOff == 1 || zOff == 1)
							if(xOff*yOff != 1 && xOff*zOff != 1 && yOff*zOff != 1)
								createChild(xOff, yOff, zOff);
						}
					}
				}
			}
		}
};


//------------------------------------------------------------------------------
/**
 * Any procedural which will be accessed via the RiProcDynamicLoad procedural
 * type must provide three functions: ConvertParameters, Subdivide, and Free;
 * here they are.
 */

/** ConvertParameters()
 *
 * Converts a string of initialization data for the procedural into whatever
 * internal data the procedural needs.  This data is sent back to the renderer
 * as an opaque pointer, and will be passed onto the Subdivide() and Free()
 * functions.
 */
extern "C" RtPointer ConvertParameters(char* initialdata)
{
	MengerSponge* params = new MengerSponge(initialdata);
	return reinterpret_cast<RtPointer>(params);
}

/** Subdivide()
 *
 * Splits the procedural into smaller primitives which are inserted
 * into the renderer pipeline via the RI.  These can be any primitive type
 * supported by the renderer, including further procedurals.
 */
extern "C" void Subdivide(RtPointer blinddata, RtFloat detailsize)
{
	const MengerSponge* p = reinterpret_cast<MengerSponge*>(blinddata);
	p->subdivide();
}

/** Free()
 *
 * Frees the data pointed to by the handle which was allocated inside
 * ConvertParameters().
 */
extern "C" void Free(RtPointer blinddata)
{
	delete reinterpret_cast<MengerSponge*>(blinddata);
}

