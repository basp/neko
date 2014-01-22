namespace Neko
{
    using System.Collections.Generic;
    using System.IO;
    using System.Text.RegularExpressions;

    public class Template
    {
        static Regex Regex = new Regex(@":([a-zA-Z_][a-zA-Z0-9_]*)");

        readonly string text;

        public Template(string text)
        {
            this.text = text;
        }

        public string Execute(IDictionary<string, object> data)
        {
            return Regex.Replace(this.text, m => Eval(m, data));
        }

        public static Template ReadEmbedded(string name)
        {
            var resourceName = string.Format("Neko.{0}", name);
            var assembly = typeof(Template).Assembly;
            using (var stream = assembly.GetManifestResourceStream(resourceName))
            using (var reader = new StreamReader(stream))
            {
                var t = reader.ReadToEnd();
                return new Template(t);
            }
        }

        private static string Eval(Match m, IDictionary<string,object> data)
        {
            var key = m.Groups[1].Captures[0].Value;
            if (data.ContainsKey(key))
            {
                return data[key].ToString();
            }

            return string.Format("<<{0}>>", key);
        }
    }
}
