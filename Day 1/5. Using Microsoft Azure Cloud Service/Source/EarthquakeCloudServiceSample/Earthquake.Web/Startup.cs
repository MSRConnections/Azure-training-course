using Microsoft.Owin;
using Owin;

[assembly: OwinStartupAttribute(typeof(Earthquake.Web.Startup))]
namespace Earthquake.Web
{
    public partial class Startup {
        public void Configuration(IAppBuilder app) {
            ConfigureAuth(app);
        }
    }
}
