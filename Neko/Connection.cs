namespace Neko
{
    using System.Collections.Generic;
    using System.Data.SqlClient;

    public class Connection
    {
        private readonly string connectionString;

        public Connection(string connectionString)
        {
            this.connectionString = connectionString;
        }

        public void Send(string queue, string msg)
        {
            var from = string.Format("{0}_initiator_svc", queue);
            var to = string.Format("{0}_target_svc", queue);
            var data = new Dictionary<string, object>
            {
                { "database", "neko" },
                { "msg" , msg },
                { "from", from },
                { "to", to }
            };

            using (var conn = new SqlConnection(this.connectionString))
            using (var cmd = conn.CreateCommand())
            {
                cmd.CommandText = Template
                    .ReadEmbedded("templates.send.sql")
                    .Execute(data);

                conn.Open();
                cmd.ExecuteNonQuery();
            }
        }

        public IEnumerable<object> Receive(string queue)
        {
            var from = string.Format("{0}_target_q", queue);
            var data = new Dictionary<string, object>
            {
                { "database", "neko" },
                { "n", 1 },
                { "queue", from }
            };

            using (var conn = new SqlConnection(this.connectionString))
            using (var cmd = conn.CreateCommand())
            {
                cmd.CommandText = Template
                    .ReadEmbedded("templates.wait_receive.sql")
                    .Execute(data);

                conn.Open();
                using (var reader = cmd.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        yield return reader[0];
                    }
                }
            }
        }
    }
}
