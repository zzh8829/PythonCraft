#ifndef _CAMERA_H_
#define _CAMERA_H_

#include "CommonInc.h"
#include "Quaternion.h"
#include "Vector3.h"
#include "Matrix4.h"

const float PI = atan(1)*4;

inline float radians(float degree)
{
	return degree*PI/180.0;
}

inline float degrees(float radians)
{
	return radians*180.0/PI;
}

class Camera
{
public:
	Camera()


	float pitchAngle;
	float yawAngle;
	float rollAngle;

	float shiftX,shiftY,shiftZ;

	Quaternion pitch,yaw,roll;

	Vector3 position,vecX,vecY,vecZ;
	Matrix4 ModelViewMatrix;

	void setPosition(float x,float y,float z)
	{
		position = Vector3(x,y,z);
		position.z = -position.z;
	}

	void setPerspective()
	{
		pitch = Quaternion(radians(pitchAngle),Vector3::UNIT_X);
		yaw = Quaternion(radians(yawAngle),Vector3::UNIT_Y);
		roll = Quaternion(radians(rollAngle),Vector3::UNIT_Z);

		Quaternion rot = pitch * yaw * roll;
		Mrot.ToRotationMatrix();


	}


};

#endif