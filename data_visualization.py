import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, Select, Button
from bokeh.plotting import figure

#function to create dataframe from each file .txt
def create_df(path, prefix=''):
    df = pd.read_csv(path, header=None, \
                    names = ['subject_id','activity_code','timestamp','x','y','z'])
    df['z'] = [ i[:-1] for i in df['z']]   #slice the "," in z value
    df['z'] = df['z'].astype(float)
    df['number'] = df.groupby(['activity_code']).cumcount()+1    #add order of each activity for merge
    df['activity_number'] = df['activity_code'] + '_' + df['number'].astype(str) #combine activity_code with number so I will have unique key value for merge
    df = df.add_prefix(prefix) #add prefix to separate with other dfs
    return df


#generate data
df_list = []

for i in list(range(1600, 1610)):  #due to the big number of data points, I'm only visualize data of 10 subjects)
    phone_accel = create_df(f'raw/phone/accel/data_{i}_accel_phone.txt', prefix='phone_accel_')  
    phone_gyro = create_df(f'raw/phone/gyro/data_{i}_gyro_phone.txt', prefix='phone_gyro_')  
    watch_accel = create_df(f'raw/watch/accel/data_{i}_accel_watch.txt', prefix='watch_accel_')
    watch_gyro = create_df(f'raw/watch/gyro/data_{i}_gyro_watch.txt', prefix='watch_gyro_')
    
    df_phone = phone_accel.merge(phone_gyro, left_on='phone_accel_activity_number', right_on = 'phone_gyro_activity_number', how='outer')
    df_watch = watch_accel.merge(watch_gyro, left_on='watch_accel_activity_number', right_on= 'watch_gyro_activity_number', how='outer')
    df_phone_watch = df_phone.merge(df_watch, left_on='phone_accel_activity_number', right_on= 'watch_accel_activity_number', how='outer')
    df_list.append(df_phone_watch)

df = pd.concat(df_list, ignore_index=True)

#function to get full subject_id and activity because the method of merge above is outer and number of rows in each sensor is different 
#so there is no column has full subject_id and activity_code
def get_full_subject_activity():
    value_subject_id = list()
    value_activity_code = list()
    for i in list(df['phone_accel_subject_id'].index):
        if pd.isnull(df.loc[i,'phone_accel_subject_id']) and pd.isnull(df.loc[i,'watch_accel_subject_id']):
            result_1 = df.loc[i,'watch_gyro_subject_id']
            result_2 = df.loc[i,'watch_gyro_activity_code']
        elif pd.isnull(df.loc[i,'phone_accel_subject_id']):
            result_1 = df.loc[i,'watch_accel_subject_id']
            result_2 = df.loc[i,'watch_accel_activity_code']
        else:
            result_1 = df.loc[i,'phone_accel_subject_id']
            result_2 = df.loc[i,'phone_accel_activity_code']
        value_subject_id.append(result_1)
        value_activity_code.append(result_2)
    return value_subject_id, value_activity_code


df['subject_id'], df['activity_code'] = get_full_subject_activity()

df = df[['subject_id', 'activity_code',
       'phone_accel_x', 'phone_accel_y', 'phone_accel_z', \
        'phone_gyro_x', 'phone_gyro_y', 'phone_gyro_z',\
        'watch_accel_x', 'watch_accel_y', 'watch_accel_z', \
        'watch_gyro_x', 'watch_gyro_y', 'watch_gyro_z']]


#frequency in each minute
minute_frequency = (1*60*1000)/50

source = ColumnDataSource(data={'x': np.arange(0, df.query("subject_id == '1600' and activity_code == 'A'").shape[0])/minute_frequency, \
				  'phone_x': df.query("subject_id == 1600 and activity_code == 'A'")['phone_accel_x'],\
				  'phone_y': df.query("subject_id == 1600 and activity_code == 'A'")['phone_accel_y'],\
				  'phone_z': df.query("subject_id == 1600 and activity_code == 'A'")['phone_accel_z'],\
				  'watch_x': df.query("subject_id == 1600 and activity_code == 'A'")['watch_accel_x'],\
				  'watch_y': df.query("subject_id == 1600 and activity_code == 'A'")['watch_accel_y'], \
				  'watch_z': df.query("subject_id == 1600 and activity_code == 'A'")['watch_accel_z']})
#create plot and widgets
plot_phone_x = figure(plot_width=800, plot_height = 200, title = 'x_axis', y_axis_label='Value')
plot_phone_x.line(x='x', y='phone_x', source = source)

plot_phone_y = figure(plot_width=800, plot_height = 200, title = 'y_axis', y_axis_label='Value', )
plot_phone_y.line(x='x', y='phone_y', source = source, color='#2f9e4d')

plot_phone_z = figure(plot_width=800, plot_height = 200, title = 'z_axis', x_axis_label ='Time in minutes', y_axis_label='Value')
plot_phone_z.line(x='x', y='phone_z', source = source, color='#e05e12')

plot_watch_x = figure(plot_width=800, plot_height = 200, title = 'x_axis', y_axis_label='Value')
plot_watch_x.line(x='x', y='watch_x', source = source)

plot_watch_y = figure(plot_width=800, plot_height = 200, title = 'y_axis', y_axis_label='Value')
plot_watch_y.line(x='x', y='watch_y', source = source, color='#2f9e4d')

plot_watch_z = figure(plot_width=800, plot_height = 200, title = 'z_axis', x_axis_label ='Time in minutes', y_axis_label='Value')
plot_watch_z.line(x='x', y='watch_z', source = source, color='#e05e12')


#create select box
select_1 = Select(options=['1600','1601','1602','1603','1604','1605','1606','1607','1608','1609'], value='1600',title = 'Subject Id (There are 51 subjects but I picked 10 subjects only due to size of data)')
select_2 = Select(options=['Walking', 'Jogging', 'Stepping on stairs', 'Sitting', 'Standing', 'Typing', 'Brushing teeth', 'Eating soup', \
							'Eating chips', 'Eating pasta', 'Drinking from cup', 'Eating sandwich', 'Kicking (soccer ball)',\
       						'Playing catch w tennis ball', 'Dribbling in basket ball', 'Writing', 'Clapping', 'Folding Clothes'], value='A',title = 'Activity')
select_3 = Select(options=['Accelerometer', 'Gyroscopy'], value='Accelerometer',title = 'Sensor')

#add callback to widgets
def callback(attr, old, new):
	s_id = select_1.value

	if select_2.value == 'Walking': activity = 'A'
	elif select_2.value == 'Jogging': activity = 'B'
	elif select_2.value == 'Stepping on stairs': activity = 'C'
	elif select_2.value == 'Sitting': activity = 'D'
	elif select_2.value == 'Standing': activity = 'E'
	elif select_2.value == 'Typing': activity = 'F'
	elif select_2.value == 'Brushing teeth': activity = 'G'
	elif select_2.value == 'Eating soup': activity = 'H'
	elif select_2.value == 'Eating chips': activity = 'I'
	elif select_2.value == 'Eating pasta': activity = 'J'
	elif select_2.value == 'Drinking from cup': activity = 'K'
	elif select_2.value == 'Eating sandwich': activity = 'L'
	elif select_2.value == 'Kicking (soccer ball)': activity = 'M'
	elif select_2.value == 'Playing catch w tennis ball': activity = 'O'
	elif select_2.value == 'Dribbling in basket ball': activity = 'P'
	elif select_2.value == 'Writing': activity = 'Q'
	elif select_2.value == 'Clapping': activity = 'R'													
	else: activity ='S'

	if select_3.value =='Accelerometer': sensor ='accel'
	else: sensor = 'gyro'

	#callback on data
	source.data = {'x': np.arange(0, df.query("subject_id == @s_id and activity_code == @activity").shape[0])/minute_frequency, \
				  'phone_x': df.query("subject_id == @s_id and activity_code == @activity")[f'phone_{sensor}_x'],\
				  'phone_y': df.query("subject_id == @s_id and activity_code == @activity")[f'phone_{sensor}_y'],\
				  'phone_z': df.query("subject_id == @s_id and activity_code == @activity")[f'phone_{sensor}_z'],\
				  'watch_x': df.query("subject_id == @s_id and activity_code == @activity")[f'watch_{sensor}_x'],\
				  'watch_y': df.query("subject_id == @s_id and activity_code == @activity")[f'watch_{sensor}_y'], \
				  'watch_z': df.query("subject_id == @s_id and activity_code == @activity")[f'watch_{sensor}_z']}


select_1.on_change('value', callback)
select_2.on_change('value', callback)
select_3.on_change('value', callback)

button_phone = Button(label='Phone', button_type="primary")
button_watch = Button(label='Watch', button_type="primary")

layout = gridplot([[select_1, None],\
				[select_2, None],\
				[select_3, None],\
				[button_phone, button_watch],\
				[plot_phone_x, plot_watch_x],\
				[plot_phone_y, plot_watch_y],\
				[plot_phone_z, plot_watch_z]])
 
curdoc().add_root(layout)

