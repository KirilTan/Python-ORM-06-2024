class RechargeEnergyMixin:
    def recharge_energy(self, amount: int) -> None:
        """
        Recharges the energy of the instance by a specified amount.

        This method increases the energy attribute of the instance by the given amount,
        ensuring that the energy does not exceed 100. After updating the energy, it saves
        the instance.

        Parameters:
        amount (int): The amount of energy to recharge. This value is added to the current
                      energy level of the instance.

        Returns:
        None
        """
        self.energy = min(100, self.energy + amount)
        self.save()
