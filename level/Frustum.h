#ifndef _FRUSTUM_H_
#define _FRUSTUM_H_

#include "math/AABB.h"
#include "SDL_opengl.h"
#include "CommonInc.h"
#include "QuadBuilder.h"

class Frustum
{
public:
	Frustum()
	{
		memset(mFrustum,0,sizeof(mFrustum));
	}

	void normalize()
	{
		for(int i=0;i!=6;i++)
		{
			double F = sqrt(
				mFrustum[i][0] * mFrustum[i][0] + 
				mFrustum[i][1] * mFrustum[i][1] + 
				mFrustum[i][2] * mFrustum[i][2]
			);
			mFrustum[i][0] /= F;
			mFrustum[i][1] /= F;
			mFrustum[i][2] /= F;
			mFrustum[i][3] /= F;
		}
	}

	void update()
	{
		glGetFloatv(GL_PROJECTION_MATRIX, mProjectionMatrix);
		glGetFloatv(GL_MODELVIEW_MATRIX, mModelViewMatrix);
		mPosition[0] = -(mModelViewMatrix[0] * mModelViewMatrix[12] + mModelViewMatrix[1] * mModelViewMatrix[13] + mModelViewMatrix[2] * mModelViewMatrix[14]);
		mPosition[1] = -(mModelViewMatrix[4] * mModelViewMatrix[12] + mModelViewMatrix[5] * mModelViewMatrix[13] + mModelViewMatrix[6] * mModelViewMatrix[14]);
		mPosition[2] = -(mModelViewMatrix[8] * mModelViewMatrix[12] + mModelViewMatrix[9] * mModelViewMatrix[13] + mModelViewMatrix[10] * mModelViewMatrix[14]);
		mClippingMatrix[0] = mModelViewMatrix[0] * mProjectionMatrix[0] + mModelViewMatrix[1] * mProjectionMatrix[4] + mModelViewMatrix[2] * mProjectionMatrix[8] + mModelViewMatrix[3] * mProjectionMatrix[12];
		mClippingMatrix[1] = mModelViewMatrix[0] * mProjectionMatrix[1] + mModelViewMatrix[1] * mProjectionMatrix[5] + mModelViewMatrix[2] * mProjectionMatrix[9] + mModelViewMatrix[3] * mProjectionMatrix[13];
		mClippingMatrix[2] = mModelViewMatrix[0] * mProjectionMatrix[2] + mModelViewMatrix[1] * mProjectionMatrix[6] + mModelViewMatrix[2] * mProjectionMatrix[10] + mModelViewMatrix[3] * mProjectionMatrix[14];
		mClippingMatrix[3] = mModelViewMatrix[0] * mProjectionMatrix[3] + mModelViewMatrix[1] * mProjectionMatrix[7] + mModelViewMatrix[2] * mProjectionMatrix[11] + mModelViewMatrix[3] * mProjectionMatrix[15];
		mClippingMatrix[4] = mModelViewMatrix[4] * mProjectionMatrix[0] + mModelViewMatrix[5] * mProjectionMatrix[4] + mModelViewMatrix[6] * mProjectionMatrix[8] + mModelViewMatrix[7] * mProjectionMatrix[12];
		mClippingMatrix[5] = mModelViewMatrix[4] * mProjectionMatrix[1] + mModelViewMatrix[5] * mProjectionMatrix[5] + mModelViewMatrix[6] * mProjectionMatrix[9] + mModelViewMatrix[7] * mProjectionMatrix[13];
		mClippingMatrix[6] = mModelViewMatrix[4] * mProjectionMatrix[2] + mModelViewMatrix[5] * mProjectionMatrix[6] + mModelViewMatrix[6] * mProjectionMatrix[10] + mModelViewMatrix[7] * mProjectionMatrix[14];
		mClippingMatrix[7] = mModelViewMatrix[4] * mProjectionMatrix[3] + mModelViewMatrix[5] * mProjectionMatrix[7] + mModelViewMatrix[6] * mProjectionMatrix[11] + mModelViewMatrix[7] * mProjectionMatrix[15];
		mClippingMatrix[8] = mModelViewMatrix[8] * mProjectionMatrix[0] + mModelViewMatrix[9] * mProjectionMatrix[4] + mModelViewMatrix[10] * mProjectionMatrix[8] + mModelViewMatrix[11] * mProjectionMatrix[12];
		mClippingMatrix[9] = mModelViewMatrix[8] * mProjectionMatrix[1] + mModelViewMatrix[9] * mProjectionMatrix[5] + mModelViewMatrix[10] * mProjectionMatrix[9] + mModelViewMatrix[11] * mProjectionMatrix[13];
		mClippingMatrix[10] = mModelViewMatrix[8] * mProjectionMatrix[2] + mModelViewMatrix[9] * mProjectionMatrix[6] + mModelViewMatrix[10] * mProjectionMatrix[10] + mModelViewMatrix[11] * mProjectionMatrix[14];
		mClippingMatrix[11] = mModelViewMatrix[8] * mProjectionMatrix[3] + mModelViewMatrix[9] * mProjectionMatrix[7] + mModelViewMatrix[10] * mProjectionMatrix[11] + mModelViewMatrix[11] * mProjectionMatrix[15];
		mClippingMatrix[12] = mModelViewMatrix[12] * mProjectionMatrix[0] + mModelViewMatrix[13] * mProjectionMatrix[4] + mModelViewMatrix[14] * mProjectionMatrix[8] + mModelViewMatrix[15] * mProjectionMatrix[12];
		mClippingMatrix[13] = mModelViewMatrix[12] * mProjectionMatrix[1] + mModelViewMatrix[13] * mProjectionMatrix[5] + mModelViewMatrix[14] * mProjectionMatrix[9] + mModelViewMatrix[15] * mProjectionMatrix[13];
		mClippingMatrix[14] = mModelViewMatrix[12] * mProjectionMatrix[2] + mModelViewMatrix[13] * mProjectionMatrix[6] + mModelViewMatrix[14] * mProjectionMatrix[10] + mModelViewMatrix[15] * mProjectionMatrix[14];
		mClippingMatrix[15] = mModelViewMatrix[12] * mProjectionMatrix[3] + mModelViewMatrix[13] * mProjectionMatrix[7] + mModelViewMatrix[14] * mProjectionMatrix[11] + mModelViewMatrix[15] * mProjectionMatrix[15];
		mFrustum[0][0] = mClippingMatrix[3] - mClippingMatrix[0];
		mFrustum[0][1] = mClippingMatrix[7] - mClippingMatrix[4];
		mFrustum[0][2] = mClippingMatrix[11] - mClippingMatrix[8];
		mFrustum[0][3] = mClippingMatrix[15] - mClippingMatrix[12];
		mFrustum[1][0] = mClippingMatrix[3] + mClippingMatrix[0];
		mFrustum[1][1] = mClippingMatrix[7] + mClippingMatrix[4];
		mFrustum[1][2] = mClippingMatrix[11] + mClippingMatrix[8];
		mFrustum[1][3] = mClippingMatrix[15] + mClippingMatrix[12];
		mFrustum[2][0] = mClippingMatrix[3] + mClippingMatrix[1];
		mFrustum[2][1] = mClippingMatrix[7] + mClippingMatrix[5];
		mFrustum[2][2] = mClippingMatrix[11] + mClippingMatrix[9];
		mFrustum[2][3] = mClippingMatrix[15] + mClippingMatrix[13];
		mFrustum[3][0] = mClippingMatrix[3] - mClippingMatrix[1];
		mFrustum[3][1] = mClippingMatrix[7] - mClippingMatrix[5];
		mFrustum[3][2] = mClippingMatrix[11] - mClippingMatrix[9];
		mFrustum[3][3] = mClippingMatrix[15] - mClippingMatrix[13];
		mFrustum[4][0] = mClippingMatrix[3] - mClippingMatrix[2];
		mFrustum[4][1] = mClippingMatrix[7] - mClippingMatrix[6];
		mFrustum[4][2] = mClippingMatrix[11] - mClippingMatrix[10];
		mFrustum[4][3] = mClippingMatrix[15] - mClippingMatrix[14];
		mFrustum[5][0] = mClippingMatrix[3] + mClippingMatrix[2];
		mFrustum[5][1] = mClippingMatrix[7] + mClippingMatrix[6];
		mFrustum[5][2] = mClippingMatrix[11] + mClippingMatrix[10];
		mFrustum[5][3] = mClippingMatrix[15] + mClippingMatrix[14];
		normalize();
	}

	int AABBInFrustum(const AABB& aabb)
	{
		return boxInFrustum(aabb.minX,aabb.minY,aabb.minZ,aabb.maxX,aabb.maxY,aabb.maxZ);
	}

	bool boxInFrustum(double minX, double minY, double minZ, double maxX, double maxY, double maxZ)
	{
		return true;
		minX = minX - mPosition[0];
		maxX = maxX - mPosition[0];
		minY = minY - mPosition[1];
		maxY = maxY - mPosition[1];
		minZ = minZ - mPosition[2];
		maxZ = maxZ - mPosition[2];


		for (int i = 0; i < 6; ++i)
		{
			if (mFrustum[i][0] * minX + mFrustum[i][1] * minY + mFrustum[i][2] * minZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * maxX + mFrustum[i][1] * minY + mFrustum[i][2] * minZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * minX + mFrustum[i][1] * maxY + mFrustum[i][2] * minZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * maxX + mFrustum[i][1] * maxY + mFrustum[i][2] * minZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * minX + mFrustum[i][1] * minY + mFrustum[i][2] * maxZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * maxX + mFrustum[i][1] * minY + mFrustum[i][2] * maxZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * minX + mFrustum[i][1] * maxY + mFrustum[i][2] * maxZ + mFrustum[i][3] <= 0.0 && 
				mFrustum[i][0] * maxX + mFrustum[i][1] * maxY + mFrustum[i][2] * maxZ + mFrustum[i][3] <= 0.0)
			{
				return false;
			}
		}

		return true;
	}

	void render()
	{
	}

	float mFrustum[16][16];
	float mClippingMatrix[16];
	float mProjectionMatrix[16];
	float mModelViewMatrix[16];
	float mPosition[3];
};

#endif