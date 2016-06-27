import unittest
import speedtest_parser


class ParserTests(unittest.TestCase):
    def test_parser(self):
        text = "Retrieving speedtest.net configuration...\n" \
               "Retrieving speedtest.net server list...\n" \
               "Testing from Bit Telecom (bittelecom.com.br) (186.216.151.120)...\n" \
               "Selecting best server based on latency...\n" \
               "'Hosted by Petrynet (Antonio Carlos) [17.86 km]: 4.079 ms'\n" \
               "Testing download speed........................................\n" \
               "Download: 14.75 Mbit/s\n" \
               "Testing upload speed..................................................\n" \
               "Upload: 9.68 Mbit/s\n" \
               "Share results: http://www.speedtest.net/result/5429694844.png\n"

        p = speedtest_parser.SpeedTestParser(text)
        expected_result = {
            'my_ip': '186.216.151.120',
            'my_server_name': 'Bit Telecom',
            'upload_speed': '9.68',
            'download_unit': 'Mbit/s',
            'my_server_domain': 'bittelecom.com.br',
            'download_speed': '14.75',
            'server_distance_unit': 'km',
            'server_ping_unit': 'ms',
            'server_ping': '4.079',
            'server_location': 'Antonio Carlos',
            'upload_unit': 'Mbit/s',
            'server_name': 'Petrynet',
            'server_distance': '17.86'
        }

        for k, v in expected_result.items():
            self.assertEqual(getattr(p, k), v, "Value for key (%s) doesn't match (%s,%s)" % (k, v, getattr(p, k)))

if __name__ == '__main__':
    unittest.main()
