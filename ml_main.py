import ml_model.ml_model as mlm

model = mlm.Model(["XAUUSD", "XAGUSD", "XPTUSD", "XPDUSD"], 12, 1)
model.train(use_generated_data=True)
model.save("model1")

