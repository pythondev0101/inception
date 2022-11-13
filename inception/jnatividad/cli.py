# from app.core.cli import core_install
# from app.auth.models import Role
# from bds.models import Municipality
# from bds import bp_bds


# @bp_bds.cli.command("install")
# def install():

#     if not core_install():
#         print("Installation failed!")
#         return False

#     if Role.query.count() <= 1:
#         role = Role()
#         role.name = "Messengers"
#         db.session.add(role)
#         print("Messenger role inserted!")

#     if Municipality.query.count() < 1:
#         mun1, mun2, mun3 = Municipality(), Municipality(), Municipality()
#         mun1.name = "Calamba"
#         mun2.name = "Binan"
#         mun3.name = "Sta.rosa"
#         db.session.add(mun1)
#         db.session.add(mun2)
#         db.session.add(mun3)
#         print("Municipalities inserted!")

#     db.session.commit()
    
#     print("Installation complete!")

#     return True