from .scaler_base import *

class LookupScaler(ScalerBase):
    """Scaler which looks up all available energies for a given surface."""

    def get_electronic_energies(self,descriptors):

        assert descriptors in self.surface_names, "Descriptor must be a surface name for LookupScaler."

        surf_idx = self.surface_names.index(descriptors)
        all_ads = self.adsorbate_names + self.transition_state_names

        E_dict = {}
        gas_names = list(self.gas_names)

        for g in gas_names:
            E_dict[g] = self.species_definitions[g]['formation_energy']

        for sp in all_ads:
            E = self.species_definitions[sp]['formation_energy'][surf_idx]
            try:
                E = float(E)
                E_dict[sp] = E 
            except ValueError: #if the energy doesn't exist for a given surface it is stored as '-'
                pass

        return E_dict

    def get_rxn_parameters(self,descriptors):
        Gs = self.get_free_energies(descriptors)
        return [Gs[d] for d in self.adsorbate_names+self.transition_state_names]
