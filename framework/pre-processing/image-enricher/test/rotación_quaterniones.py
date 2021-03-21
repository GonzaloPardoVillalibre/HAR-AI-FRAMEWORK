import numpy as np

def unitary_rotation_quaternion(x:float, y:float, z:float, a:float)
    rotation_factor = np.sin( a / 2 )

    x = x * rotation_factor
    y = y * rotation_factor
    z = z * rotation_factor

    w = cos( a / 2 )


# Dado un quaternión "omega" entonces  -> La rotación de dicho cuaternión 15 grados sobre el eje Y sería
omega
vector_de_rotacion =  unitary_rotation_quaternion(0,0,1, 15*np.pi/180)
quaternion_final = vector_de_rotacion * omega
