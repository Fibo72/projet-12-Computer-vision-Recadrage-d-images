import  pycpd as cpd

# create a RigidRegistration object

reg = cpd.RigidRegistration(X=target, Y=source)

# run the registration & collect the results

TY, (s_reg, R_reg, t_reg) = reg.register()

# TY is the transformed source points
# the values in () are the registration parameters.
# In this case of rigid registration they are:
#     s_reg the scale of the registration
#     R_reg the rotation matrix of the registration
#     t_reg the translation of the registration