# groheblue
A python package for interacting with the Grohe Blue API. The API uses the Grohe IOT API which is used by the Grohe Blue app. The API is not publicly documented and may change at any time. I am not affiliated with Grohe or the Grohe Blue app in any way.

## Restrictions
* The package currently only officially supports the **Grohe Blue Home** device, because this is the only one I have. If you have a **Grohe Blue Professional** device and can verify the functionality, please contact me.

## Installation
```
pip install groheblue
```

## Usage
```python
from groheblue import GroheClient

client = GroheClient("<EMAIL>", "<PASSWORD>")


async def main():
    await client.login()

    devices = await client.get_devices()  # get all devices
    device = devices[0]  # select the first device

    # To see all available data, look into the classes.py file. Here are some example values:
    print(device.appliance_id)  # print the appliance id of the device

    print(device.data_latest.remaining_co2)  # print the remaining co2 of the device in %

    print(device.data_latest.remaining_filter)  # print the remaining filter of the device in %

    print(device.config.co2_consumption_carbonated)  # print the co2 consumption for carbonated water

    await client.dispense(device, 1, 50)  # dispense 50ml of still water

    await client.dispense(device, 3, 200) # dispense 200ml of carbonated water


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

```

## Acknowledgments

* <lennartkaden> [lennartkaden](https://github.com/lennartkaden/Grohe-Blue-API-Python.git) for his work on the Grohe-Blue-API-Python. His work significantly contributed to me being able to write this package.

## License
This project is licensed under the <MIT> [MIT](https://github.com/koproductions-code/groheblue/blob/master/LICENSE) License - see the LICENSE file for details.