from atlas.typing.typer.base import Typer


class PresenceTyper(Typer):

	def __init__(self, depths, contamination_depths = []):
		super(PresenceTyper, self).__init__(depths, contamination_depths)

	def type(self, genes):
		typed_as_present = {}
		for gene_name, gene_versions in genes.iteritems():
			best_gene_version = self.get_best_gene_version(gene_versions.values())
			if best_gene_version.percent_coverage > 30:
				typed_as_present[gene_name] = best_gene_version
		return typed_as_present

	def get_best_gene_version(self, genes):
		genes.sort(key=lambda x: x.percent_coverage, reverse=True)
		current_best_gene = genes[0]
		for gene in genes[1:]:
			if gene.percent_coverage < current_best_gene.percent_coverage:
				return current_best_gene
			else:
				if gene.median_depth > current_best_gene.median_depth:
					current_best_gene = gene
		return current_best_gene