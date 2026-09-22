import time, datetime
from h2o_wave import site, ui, data
import psutil
import speedtest # speedtest-cli


def bits_to_mbps(bits):
    return round(bits / 1_000_000, 2)


if __name__ == "__main__":
    page = site['/']
    tick = 0

    speed_test = speedtest.Speedtest(secure=True)
    download_speed = bits_to_mbps(speed_test.download())
    upload_speed = bits_to_mbps(speed_test.upload())

    cpu_card = page.add('cpu_stats', ui.small_series_stat_card(
        box='1 1 2 2',
        title='CPU',
        value='={{usage}}%',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$red',
    ))

    core_card = page.add('cpu_cores', ui.small_series_stat_card(
        box='3 1 2 2',
        title='CPU Cores',
        value='={{usage}}',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$purple',
    ))

    mem_card = page.add('mem_stats', ui.small_series_stat_card(
        box='1 3 2 2',
        title='Memory',
        value='={{usage}}%',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$blue',
    ))

    battery_card = page.add('battery_stats', ui.small_series_stat_card(
        box='3 3 2 2',
        title='Battery',
        value='={{usage}} %',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$pink',
    ))

    temp_card = page.add('temp_stats', ui.small_series_stat_card(
        box='3 5 2 2',
        title='Heat',
        value='={{usage}} °C',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$yellow',
    ))

    boot_card = page.add('boot_stats', ui.small_series_stat_card(
        box='3 7 2 2',
        title='Last Boot',
        value='={{usage}}',
        data=dict(usage=0.0),
        plot_data=data('tick usage', -15),
        plot_category='tick',
        plot_value='usage',
        plot_zero_value=0,
        plot_color='$cyan',
    ))
    
    download_card = page.add('download_speed', ui.small_series_stat_card(
        box='1 5 2 2',
        title='Download speed',
        value=f"{download_speed} Mbps",
        data=dict(download_speed=0.0),
        plot_data=data('tick speed', -15),
        plot_category='tick',
        plot_value='speed',
        plot_zero_value=0,
        plot_color='$orange',

    ))

    upload_card = page.add('upload_speed', ui.small_series_stat_card(
        box='1 7 2 2',
        title='Upload speed',
        value=f"{upload_speed} Mbps",
        data=dict(upload_speed=0.0),
        plot_data=data('tick speed', -15),
        plot_category='tick',
        plot_value='speed',
        plot_zero_value=0,
        plot_color='$green',

    ))

    while True:        
        tick += 1

        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_card.data.usage = cpu_usage
        cpu_card.plot_data[-1] = [tick, cpu_usage]

        mem_usage = psutil.virtual_memory().percent
        mem_card.data.usage = mem_usage
        mem_card.plot_data[-1] = [tick, mem_usage]

        cpu_count = psutil.cpu_count()
        core_card.data.usage = cpu_count
        core_card.plot_data[-1] = [tick, cpu_count]

        battery_values = psutil.sensors_battery()
        battery_level = f"{battery_values.percent:.2f}"
        battery_card.data.usage = battery_level
        battery_card.plot_data[-1] = [tick, battery_values.percent]

        temperature_values = psutil.sensors_temperatures()
        # hardcored sensor name for Linux, Lenovo T16 G1
        current_temp = temperature_values['coretemp'][0].current
        temp_card.data.usage = current_temp
        temp_card.plot_data[-1] = [tick, current_temp]

        boot_time = psutil.boot_time()
        bt = (datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S"))
        boot_card.data.usage = bt
        boot_card.plot_data[-1] = [tick, boot_time]

        # perform speed test every 10 ticks (10 seconds)
        if tick % 10 == 0:
            download_speed = bits_to_mbps(speed_test.download())
            download_card.data.usage = str(download_speed)
            download_card.value = f"{download_speed} Mbps"
            download_card.plot_data[-1] = [tick, str(download_speed)]
            upload_speed = bits_to_mbps(speed_test.upload())
            upload_card.data.usage = str(upload_speed)
            upload_card.value = f"{upload_speed} Mbps"
            upload_card.plot_data[-1] = [tick, str(upload_speed)]

        page.save()
        time.sleep(1)


