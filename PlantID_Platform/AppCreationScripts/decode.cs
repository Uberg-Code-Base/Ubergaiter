string sharingUrl = "https://1drv.ms/f/s!AhEY2igzgu3nh692EzFUk2BCDPXEEQ";
string base64Value = System.Convert.ToBase64String(System.Text.Encoding.UTF8.GetBytes(sharingUrl));
string encodedUrl = "u!" + base64Value.TrimEnd('=').Replace('/','_').Replace('+','-');

print(encodedUrl)