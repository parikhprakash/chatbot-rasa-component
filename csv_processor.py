from custom_entities import entity_types, sample_utterances, synonymns_agg_type
import random

#entity_columns
columns = ['name','pay','position','dept','eng_score']
dimension_columns = ['position','dept']
metrics_columns = ['pay','eng_score']

entity_names = dimension_columns
entity_possible_values = {}
import pandas as pd

df = pd.read_csv('sample_dataset_chatbot.csv')
for dim_entity in entity_names:
    entity_possible_values[dim_entity] = list(df[dim_entity].unique())

entity_possible_values['metric'] = metrics_columns

#generate sampled entity_possible_values
sampled_entity_possible_values = {}
for key in entity_possible_values:
    if len(entity_possible_values[key]) > 5:
       sampled_entity_possible_values[key] = random.sample(entity_possible_values[key],int(len(entity_possible_values[key])*0.8))
    else:
        sampled_entity_possible_values[key]  =entity_possible_values[key]

final_utterances = []
dim_temp_utterances = []
for utter in sample_utterances:
    if "(dimension)" in utter:
        for dim in dimension_columns:
            for val in sampled_entity_possible_values[dim]:
                new_utter = utter.replace("(dimension)","[{}]({})".format(val,dim))
                dim_temp_utterances.append(new_utter)
metric_temp_utterances = []
for utter in dim_temp_utterances:
    if "(metric)" in utter:
        for metric in metrics_columns:
            new_utter = utter.replace("(metric)","[{}](metric)".format(metric))
            metric_temp_utterances.append(new_utter)

for utter in metric_temp_utterances:
    if "(agg)" in utter:
        for agg_type in entity_types['agg']:
            new_utter = utter.replace("(agg)","[{}](agg)".format(agg_type))
            final_utterances.append(new_utter)

with open("data/template.txt","r") as template_md:
    data = template_md.read()
    with open("data/nlu.md","w") as final_md:
        final_md.write(data)
        final_md.write("\n")
        final_md.write("## intent:query_db\n")
        final_md.write("\n".join(final_utterances))
        final_md.write("\n")
        ## synonym:
        for syn_mapper in synonymns_agg_type.keys():
            final_md.write("## synonym:{}\n".format(syn_mapper))
            for syn in synonymns_agg_type[syn_mapper]:
                final_md.write("- {}\n".format(syn))
            final_md.write("\n")

