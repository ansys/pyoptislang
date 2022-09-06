* ------------------------------------------------------------------------------------------------------------------
*
*   DYNARDO example (c) Dynardo 2012
*
*   ten bar truss (Haftka & Guerdal 1992)
*
*   Minimize the mass
*   0.1 <= a_i <= 20 in^2
*   Maximum stress is 25000
*
* ------------------------------------------------------------------------------------------------------------------ /

* Define cross section areas /
object create,real,,area01/     * Optimal value = 7.94 /
object create,real,,area02/     * Optimal value = 0.10 /
object create,real,,area03/     * Optimal value = 8.06 /
object create,real,,area04/     * Optimal value = 3.94 /
object create,real,,area05/     * Optimal value = 0.10 /
object create,real,,area06/     * Optimal value = 0.10 /
object create,real,,area07/     * Optimal value = 5.74 /
object create,real,,area08/     * Optimal value = 5.57 /
object create,real,,area09/     * Optimal value = 5.57 /
object create,real,,area10/     * Optimal value = 0.10 /

object read,,area01 10.00000,/
object read,,area02 10.00000,/
object read,,area03 10.00000,/
object read,,area04 10.00000,/
object read,,area05 10.00000,/
object read,,area06 10.00000,/
object read,,area07 10.00000,/
object read,,area08 10.00000,/
object read,,area09 10.00000,/
object read,,area10 10.00000,/

* Material properties /
object create,real,,Youngs/
object create,real,,density/
object read,,Youngs 10000000,/
object read,,density 0.100000,/

* Loads /
object create,real,,F1/
object create,real,,F2/
object read,,F1 -100000.000,/
object read,,F2 -100000.000,/

* Length /
object create,real,,L/
object read,,L 360,/

* Calculate mass /
object create,real,,mass/
object read,,mass \mul \mul L density \add area01 \add area02 \add area03 \add area04 \add area05 \add area06 \mul \sqr 2 \add area07 \add area08 \add area09 area10,/

* Define global vectors, dofs, incidences /
object create,real vector,10,areas/
object read,, areas area01 area02 area03 area04 area05 area06 area07 area08 area09 area10,/

object extract, minimum, areas, min_area min_row/
control if,less real,min_area 0 write_error,/

object create,real matrix,6 2,node_coordinates/
object read,, node_coordinates
\mul 2 L L
\mul 2 L 0
L L
L 0
0 L
0 0,/
object create, matrix,10 2,element_incidences/
object read,, element_incidences
3 5
1 3
4 6
2 4
3 4
1 2
4 5
3 6
2 3
1 4,/
object create,,,num_nodes/
object read,, num_nodes 6,/
object create,,,num_elements/
object read,, num_elements 10,/
object create,vector,8,available_dof/
object read,, available_dof 1 2 3 4 5 6 7 8,/
object create,,,num_available_dof/
object read,, num_available_dof 8,/
object create,real vector,12,global_load/
object read,, global_load
0 0 0 F2 0 0 0 F1 0 0 0 0,/

* Remove node 1 from dof list, if unimportant trusses are set to zero/
control if, real greater, \add area02 \add area06 area10 0 jump_remove_node1,/
    object create,replace vector,6,available_dof/
    object read,, available_dof 3 4 5 6 7 8,/
    object read,, num_available_dof 6,/
#label jump_remove_node1

* Build up global stiffness /
object create,,,element_count/
object copy,,num_nodes,num_nodes2/
object modify,multiply,num_nodes2 2,/
object create, real matrix, num_nodes2 num_nodes2,global_stiffness/
object create, real matrix, 2 2,local_stiffness_init/
object create, real matrix, 2 4,trafo_matrix/
object read,,local_stiffness_init 1 -1 -1 1,/
#label element_loop_stiffness
    object modify, add, element_count 1,/
    object extract, replace row,element_incidences element_count, nodes/
    object extract, replace row, nodes 1,node1/
    object extract, replace row, nodes 2,node2/
    object extract, replace row, node_coordinates node1,coor_node1/
    object extract, replace row, node_coordinates node2,coor_node2/
    object extract, replace row, areas element_count,area/

    * Local element stiffness /
    object combine,\sub replace,coor_node2 coor_node1 ,coor_diff/
    linalg norm, replace,coor_diff, length/
    object operate,\div,coor_diff length,/
    object copy,replace,local_stiffness_init,local_stiffness/
    object operate,\mul, local_stiffness \div \mul Youngs area length,/

    * Transform local stiffness to global coordinates /
    object read,,trafo_matrix coor_diff 1 coor_diff 2 0 0 0 0 coor_diff 1 coor_diff 2,/
    linalg multiply, trans_first replace,trafo_matrix local_stiffness,help_stiffness/
    linalg multiply, replace, help_stiffness trafo_matrix,element_stiffness/

    * Assemble element matrix in global matrix /
    object create,replace,,dof_count1/
    #label dof_loop1
        object create,replace,,dof_count2/
        object modify, add, dof_count1 1,/
        #label dof_loop2
            object modify, add, dof_count2 1,/
            object extract,row replace, nodes dof_count1,pos1/
            object extract,row replace, nodes dof_count2,pos2/
            object modify,multiply,pos1 2,/
            object modify,subtract,pos1 1,/
            object modify,multiply,pos2 2,/
            object modify,subtract,pos2 1,/

            object copy,replace,dof_count1,pos1_local/
            object copy,replace,dof_count2,pos2_local/
            object modify,multiply,pos1_local 2,/
            object modify,subtract,pos1_local 1,/
            object modify,multiply,pos2_local 2,/
            object modify,subtract,pos2_local 1,/

            object modify,set,global_stiffness pos1 pos2 \add global_stiffness pos1 pos2 element_stiffness pos1_local pos2_local,/
            object modify,add,pos2 1,/
            object modify,add,pos2_local 1,/
            object modify,set,global_stiffness pos1 pos2 \add global_stiffness pos1 pos2 element_stiffness pos1_local pos2_local,/
            object modify,add,pos1 1,/
            object modify,subtract,pos2 1,/
            object modify,add,pos1_local 1,/
            object modify,subtract,pos2_local 1,/
            object modify,set,global_stiffness pos1 pos2 \add global_stiffness pos1 pos2 element_stiffness pos1_local pos2_local,/
            object modify,add,pos2 1,/
            object modify,add,pos2_local 1,/
            object modify,set,global_stiffness pos1 pos2 \add global_stiffness pos1 pos2 element_stiffness pos1_local pos2_local,/

        control if,integer less,dof_count2 2 dof_loop2,/
    control if,integer less,dof_count1 2 dof_loop1,/
    *control exit,,,/
control if,integer less,element_count num_elements element_loop_stiffness,/

* Reduced global stiffness and loads according to free dofs /
object extract,row byindex,global_stiffness available_dof,global_stiffness_help/
object extract,column byindex,global_stiffness_help available_dof,global_stiffness_reduced/
object extract,row byindex,global_load available_dof,global_load_reduced/

* Solve linear equation, extract global displacements /
linalg solve,,global_stiffness_reduced global_load_reduced,global_disp_reduced/
object create,real vector,12,global_disp/
object assemble,row byindex,global_disp_reduced global_disp available_dof,/

object create,replace,,element_count/
object create, real vector replace, 4,disp_matrix/
object create, real vector replace, 10,element_stresses/
#label element_loop_stress
    object modify, add, element_count 1,/

    object extract, replace row,element_incidences element_count, nodes/
    object extract, replace row, nodes 1,node1/
    object extract, replace row, nodes 2,node2/
    object extract, replace row, node_coordinates node1,coor_node1/
    object extract, replace row, node_coordinates node2,coor_node2/
    object extract, replace row, areas element_count,area/
    object combine,\sub replace,coor_node2 coor_node1 ,coor_diff/
    linalg norm, replace,coor_diff, length/
    object operate,\div,coor_diff length,/
    object read,,trafo_matrix coor_diff 1 coor_diff 2 0 0 0 0 coor_diff 1 coor_diff 2,/

    object copy,replace,node1,pos1/
    object copy,replace,node2,pos2/
    object modify,multiply,pos1 2,/
    object modify,multiply,pos2 2,/
    object copy,replace,pos1,pos3/
    object copy,replace,pos2,pos4/
    object modify,subtract,pos1 1,/
    object modify,subtract,pos2 1,/
    object read,,disp_matrix global_disp pos1 global_disp pos3 global_disp pos2 global_disp pos4,/
    linalg multiply, replace, trafo_matrix disp_matrix,disp_local/
    object create,replace real,,stress/
    object read,,stress \mul Youngs \div \sub disp_local 2 disp_local 1 length,/
    object modify,set,element_stresses element_count stress,/
control if,integer less,element_count num_elements element_loop_stress,/
object copy,,global_disp,global_disp_abs/
object operate,\abs,global_disp_abs,/
object extract,maximum,global_disp_abs,max_disp row1/

object copy,,element_stresses,element_stresses_abs/
object operate,\abs,element_stresses_abs,/
object extract,maximum,element_stresses_abs,max_stress row2/

output print,,mass,/
output print,,max_disp,/
output print,,max_stress,/
output print,,global_disp,/
output print,,element_stresses,/

* Write output file /
file open, write plain text, "ten_bar_truss.out", theFile /

file write, string, theFile "Mass", /
file write, format, theFile mass "%16.5f", /
file write, string, theFile "", /
file write, string, theFile "Maximum vertical displacement", /
file write, format, theFile max_disp "%16.5f", /
file write, string, theFile "", /
file write, string, theFile "Maximum element stress", /
file write, format, theFile max_stress "%16.5f", /

* displacements /
object create,,, node_count /
object create,,, node_count2 /
#label node_write_loop
    object modify, add, node_count 1, /
    object modify, add, node_count2 2, /
    file write, string, theFile "", /
    string convert, replace int_string no_space, node_count, szTMP /
    string append, replace, 2 "Vertical displacement node " szTMP, szTmp2 /
    file write, string, theFile szTmp2, /

    object extract, replace row, global_disp node_count2, disp_node /
    file write, format, theFile disp_node "%16.5f", /
control if, less, node_count2  8   node_write_loop, /
object delete,, node_count2, /
object delete,, node_count, /

* stresses /
object read,, element_count 0, /
#label element_write_loop
    object modify, add, element_count 1, /
    file write, string, theFile "", /
    string convert, int_string no_space replace, element_count, szTMP /
    string append, replace, 2 "Stress element " szTMP, szTmp2 /
    file write, string, theFile szTmp2, /

    object extract, row replace, element_stresses element_count, element_stress /
    file write, format, theFile element_stress "%16.5f", /
control if, less, element_count  num_elements   element_write_loop, /
object delete,, element_count, /

file write, string, theFile "", /
file write, string, theFile "Calculation completed successfully", /

file close,, theFile, /

control quit,,,/

#label write_error
string append, replace, 1 "Negative area(s)", szTmp /
output file, text plain string, szTmp, ten_bar_truss.err /
control quit,,,/
