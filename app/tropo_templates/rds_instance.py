from troposphere import (
    rds,
    Ref,
)

from parameters import (
    subnet_ids,
    rds_master_password,
    rds_master_username,
    rds_db_name,
)

# RDSInstance = {
#     "Type": "AWS::RDS::DBInstance",
#     "Properties": {
#         "VPCSecurityGroups": [
#             {
#                 "Fn::GetAtt": "RDSSecurityGroup.GroupId"
#             }
#         ],
#     },
# }
rds_subnet_group = rds.DBSubnetGroup(
    "RDSSubnetGroup",
    DBSubnetGroupDescription="RDS Subnet's Group",
    SubnetIds=Ref(subnet_ids)
)

rds_instance = rds.DBInstance(
    "RDSInstance",
    # VPCSecurityGroups=[]
    DBSubnetGroupName=Ref(rds_subnet_group),
    AllocatedStorage=5,
    DBInstancEClass="db.t2.micro",
    Engine="postgres",
    MasterUsername=Ref(rds_master_username),
    MasterUserPassword=Ref(rds_master_password),
    DBName=Ref(rds_db_name),
    DeletionPolicy="Delete",
)
