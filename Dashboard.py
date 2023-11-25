import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st 
import plotly.express as px 
import os
import seaborn as sns

dataset=pd.read_csv('./data/order_payment_dataset.csv')

st.set_page_config(page_title="Order Payment analysis",layout="wide")

st.sidebar.header("filter By:")

payment_type=st.sidebar.multiselect("payment_type",
                                 options = dataset["payment_type"].unique(),
                                 default=dataset["payment_type"].unique())

selection_query=dataset.query(
    "payment_type== @payment_type"
)

st.title("E-Commerce Order Payment")

#st.dataframe(selection_query)

total_payment=(selection_query["payment_value"].sum())
Average_payment=round(selection_query["payment_value"].mean())


first_column,second_column=st.columns(2)

with first_column:
    st.markdown("### Total Payment:")
    st.subheader(f'{total_payment}$')
with second_column:
    st.markdown("### Average Payment:")
    st.subheader(f'{Average_payment}$')

st.markdown("---")

st.title("Payment_Installments")

payment_installments=(selection_query.groupby(by=["payment_installments"]).sum()[["payment_value"]])


payment_installments_barchart=px.bar(payment_installments,
                                x=payment_installments.index,
                                y="payment_value",
                                title="Total Payment by Installment")
                                #color_discrete_sequence=["ff0000"],
                                #)

payment_installments_barchart.update_layout(plot_bgcolor = "rgb(255,0,0)",xaxis=(dict(showgrid=False)))


payment_installments_piechart=px.pie(payment_installments, names= payment_installments.index,values="payment_value",title="Percentage Payment installments",hole=.3,color=payment_installments.index,color_discrete_sequence=px.colors.sequential.RdPu_r)


left_column,right_column=st.columns(2)
left_column.plotly_chart(payment_installments_piechart,use_container_width=True)
right_column.plotly_chart(payment_installments_barchart,use_container_width=True)


st.markdown("---")

num_columns = ['order_id', 'payment_sequential', 'payment_type',
       'payment_installments', 'payment_value']

cat_columns = [None, 'Type', 'AirBags', 'Origin', 'DriveTrain' 'Cylinders']

st.title("Scatter Plot for  E-Commerce Order Payment Sequential")

col1, col2 = st.columns ([0.25,0.75])

with col1:
    x_axis = st.selectbox('X-Axis:',
                          num_columns,index =0)
    y_axis = st.selectbox('Y-Axis:',
                          num_columns, index=1)
    c_axis = st.selectbox('Colour:', cat_columns)

with col2:
    fig, ax = plt.subplots()
    sns.scatterplot(x=x_axis, y=y_axis, hue=c_axis,
                   data=dataset)
    st.pyplot(fig)
    #sns.scatterplot(x=dataset[x_axis], y=dataset[y_axis], hue=dataset[c_axis], palette='viridis', s=60)
    #plt.title('Scatter Plot for E-Commerce Order Payment Sequential')
    #plt.xlabel(x_axis)
    #plt.ylabel(y_axis)
    #st.pyplot(fig)