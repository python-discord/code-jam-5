import datetime


class FarmerTownMain:
    """FarmerTown account object.

    Attributes
    ------------
    id: int
        The row ID
    user_id: int
        The user ID of account owner
    farmer_name: str
        The owner's farmer name
    cash: int
        The account balance
    """
    __slots__ = ('db', 'result', 'id', 'user_id', 'farmer_name', 'cash', 'debt', 'banked')

    def __init__(self, db, result):
        self.db = db
        self.result = result

        self.id: int = result['id']
        self.user_id: int = result['user_id']
        self.farmer_name: str = result['farmer_name']
        self.cash: int = result['cash'] or 0
        self.debt: int = result['debt'] or 0
        self.banked: int = result['banked'] or 0

    @property
    def last_used(self):
        """Return a datetime timestamp for last time command was used.
        """
        raw = self.result['last_used']
        if not raw:
            return None

        return datetime.datetime.fromtimestamp(raw)

    async def update_last_used(self):
        """Update the last time used to be now.
        """
        now = datetime.datetime.now()

        def execute():
            self.db.connection.execute("UPDATE farmertown SET last_used=? WHERE user_id=?",
                                       (now.timestamp(), self.user_id)
                                       )
            self.db.connection.commit()

        return await self.db.loop.run_in_executor(None, execute)

    async def remove_last_used(self):
        """Remove the last time used.
        """
        def execute():
            self.db.connection.execute("UPDATE farmertown SET "
                                       "last_used=NULL WHERE user_id=?",
                                       (self.user_id,
                                        )
                                       )
            self.db.connection.commit()
        return await self.db.loop.run_in_executor(None, execute)

    async def new_decision(self, crop_name, drought, germination, profit, loss):
        """Create a new decision for the user ID.
        Decisions are made with the `>farmertown sow` command.

        Parameters
        ----------------
        crop_name: str
            The name of the crop sown
        drought: bool
            Whether the drought occured or not
        germination: float
            The germination rate of the crop
        profit: int
            The amount of money profit made.
        loss: int
            The loss incurred.
        """
        def execute():
            self.db.connection.execute("INSERT INTO farmerdecisions "
                                       "(user_id, crop_name, drought,"
                                       " germination, profit, loss, used)"
                                       " VALUES (?, ?, ?, ?, ?, ?, ?)",
                                       (self.user_id,
                                        crop_name,
                                        drought,
                                        germination,
                                        profit,
                                        loss,
                                        datetime.datetime.now().timestamp())
                                       )
            self.db.connection.commit()
        return await self.db.loop.run_in_executor(None, execute)

    async def last_decision(self):
        """Retrieve the last decision made by the user.
        """
        def execute():
            return self.db.connection.execute("SELECT * FROM farmerdecisions WHERE user_id = ? "
                                              "ORDER BY used DESC LIMIT 1;", (self.user_id, ))
        result = await self.db.loop.run_in_executor(None, execute)
        for row in result:
            return FarmerTownDecision(row)

    async def update_accounts(self):
        """Update the accounts to include the last decision made.
        """
        last_decision = await self.last_decision()

        def execute():
            to_add = last_decision.profit - last_decision.loss + self.cash
            self.db.connection.execute(
                "UPDATE farmertown SET cash=? WHERE user_id=?",
                (to_add, self.user_id)
            )

            self.db.connection.commit()

        return await self.db.loop.run_in_executor(None, execute)


class FarmerTownDecision:
    """Represents a FarmerTown decision.
    Decisions are made when the user calls `>farmertown sow`.

    Attributes
    -------------
    id: int
        The row ID
    user_id: int
        The account owner's ID
    crop_name: str
        The name of crop sown.
    drought: bool
        Whether the decision incurred a drought.
    germination: int
        The germination rate of the crop.
    profit: int
        The profit attained.
    loss: int
        The losses incurred.
    """
    __slots__ = ('result', 'id', 'user_id', 'crop_name', 'drought', 'germination', 'profit', 'loss')

    def __init__(self, result):
        self.result = result

        self.id = result['id']
        self.user_id = result['user_id']
        self.crop_name = result['crop_name']
        self.drought = result['drought']
        self.germination = result['germination']
        self.profit = result['profit']
        self.loss = result['loss']

    @property
    def used(self):
        """Returns a datetime timestamp of when the decision was made."""
        raw = self.result['used']
        return datetime.datetime.fromtimestamp(raw)
