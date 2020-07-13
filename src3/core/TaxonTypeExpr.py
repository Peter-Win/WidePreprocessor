from Taxon import Taxon


# +-----+        +----------+
# | Var |------->| TypeExpr |
# +-----+        |----------|
#                |  attrs   |
#                +----------+
#                 Δ
#                 |
#  +--------------+
#  | TypeExprName |
#  +--------------+
#  | nameRef: str |
#  +--------------+
#         |
#         v
# Scalar, Class, enum, typedef

class TaxonTypeExpr(Taxon):
	pass