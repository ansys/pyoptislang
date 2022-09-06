* ---------------------------------------------------------------------------------------------- /
*                                                                                                /
* Dynardo example (c) Dynardo 2011                                                               /
*                                                                                                /
* Damped oscillator                                                                               /
*                                                                                                /
* Undamped eigenfrequency: omega_0 = sqrt(k div m)                                               /
* Damped eigenfrequency:     omega = sqrt(1-D^2)*omega_0                                         /
* Response:                   x(t) = exp(-D*omega_0*t)*sqrt(2*Ekin div m) div omega*sin(omega*t) /
*                                                                                                /
* Minimize maximum amplitude after 5 seconds                                                     /
* Maximum eigenfrequencies as constraint: omega <= 8                                             /
*                                                                                                /
* 0.1 <= m <= 5.0                                                                                /
* 10  <= k <= 50                                                                                 /
* D = 0.02                                                                                       /
* Ekin = 10                                                                                      /
*                                                                                                /
* ---------------------------------------------------------------------------------------------- /

object create,real,,m/
object create,real,,k/
object create,real,,D/
object create,real,,Ekin/

object read,,m 1.000000,/
object read,,k 20.000000,/
 
object read,,D 0.020000,/
object read,,Ekin 10.000000,/


* initial velocity /
object create,real replace,,v0/
object read,,v0 \sqr \div \mul 2 Ekin m,/
*output print,,v0,/

* undamped and damped eigen frequency /
object combine,\div replace,k m,omega0/
object operate,\sqr,omega0 ,/
object copy, replace,omega0,omega_damped/
object operate,\mul,omega_damped \sqr \sub 1 \pow D 2 ,/
*output print,,omega0,/
output print,,omega_damped,/

object create,,,num_steps/
object read,,num_steps 100,/
object create,real,,t_max/
object read,,t_max 10,/
object create,real,,t_observe/
object read,,t_observe 5,/

* envelope approximation of maximum amplitude /
object copy, replace,t_observe,x_max_env/
object operate,\mul,x_max_env \mul D omega0,/
object operate,\chs,x_max_env,/
object operate,\exp,x_max_env,/
object operate,\mul,x_max_env \div v0 omega_damped,/
*output print,,x_max_env,/

* time series /
object create,real vector,num_steps,t_values/
object initialize,linear_column,t_values 0 t_max,/

object copy, replace,t_values,sin_values/
object operate,\mul,sin_values omega_damped ,/
object operate,\sin,sin_values,/

object copy, replace,t_values,envelope/
object operate,\mul,envelope \mul D omega0,/
object operate,\chs,envelope,/
object operate,\exp,envelope,/
object operate,\mul,envelope \div v0 omega_damped,/
object combine,\mul,sin_values envelope,x_values/

* extract maximum amplitude from time series/
object copy, replace,t_values,indicator/
object operate,\geq,indicator t_observe,/
object combine,\mul,indicator x_values,x_values_indicator/
object operate,\abs,x_values_indicator,/
object extract,maximum replace,x_values_indicator,x_max row/
output print,,x_max,/
object append,add_columns,t_values x_values,/
object copy,replace,t_values,signal/

string append,,1 "omega_damped",string_omega/
string append,,1 "
x_max",string_xmax/
output file,plain text string,string_omega,oscillator_solution.txt/
output file,plain text freeformat append,omega_damped " %2.5f",oscillator_solution.txt/
output file,plain text string append,string_xmax,oscillator_solution.txt/
output file,plain text freeformat append,x_max " %2.5f",oscillator_solution.txt/

string append,,1 "  Simulation
  time     displacement 
",string_signal/
output file,plain text string,string_signal,oscillator_signal.txt/
output file,plain text freeformat append,signal "  %2.5f",oscillator_signal.txt/


control quit,,,/
