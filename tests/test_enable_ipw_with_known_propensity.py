from causallift import CausalLift

from sklearn.model_selection import train_test_split

seed = 0

from causallift import generate_data

df = generate_data( \
    N=1000,
    n_features=3,
    beta=[0, -2, 3, -5],  # Effect of [intercept and features] on outcome
    error_std=0.1,
    tau=[1, -5, -5, 10],  # Effect of [intercept and features] on treated outcome
    tau_std=0.1,
    discrete_outcome=True,
    seed=seed,
    feature_effect=0,  # Effect of beta on treated outxome
    propensity_coef=[0, -1, 1, -1],  # Effect of [intercept and features] on propensity log-odds for treatment
    index_name='index')

train_df, test_df = train_test_split(df, test_size=0.2, random_state=seed, stratify=df['Treatment'])

test_random_propensity = True

if test_random_propensity:
    import random
    train_df = train_df.copy()
    train_df.loc[:,'Propensity'] = [random.random() for _ in range(train_df.shape[0])]

    test_df = test_df.copy()
    test_df.loc[:,'Propensity'] = [random.random() for _ in range(test_df.shape[0])]

cl = CausalLift(train_df, test_df, enable_ipw=True, random_state=0, verbose=3)
train_df, test_df = cl.estimate_cate_by_2_models()
estimated_effect_df = cl.estimate_recommendation_impact()

