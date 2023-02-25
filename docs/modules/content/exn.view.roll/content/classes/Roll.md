Back to [All Modules](https://github.com/pyrustic/exn/blob/master/docs/modules/README.md#readme)

# Module Overview

**exn.view.roll**
 
No description

> **Classes:** &nbsp; [EntriesList](https://github.com/pyrustic/exn/blob/master/docs/modules/content/exn.view.roll/content/classes/EntriesList.md#class-entrieslist) &nbsp;&nbsp; [Roll](https://github.com/pyrustic/exn/blob/master/docs/modules/content/exn.view.roll/content/classes/Roll.md#class-roll)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; None

# Class Roll
Subclass this if you are going to create a view.

Lifecycle of a view:
    1- you instantiate the view
    2- '__init__()' is implicitly called
    3- you call the method '.build()'
    4- '_build()' is implicitly called
    5- '_on_map()' is implicitly called once the widget is mapped
    6- '_on_destroy()' is implicitly called when the widget is destroyed/closed

The rules to create your view is simple:
- You need to subclass Viewable.
- You need to implement the methods '_build()', and optionally
    implement '_on_map()' and '_on_destroy()'.
- You need to set an instance variable '_body' with either a tk.Frame or tk.Toplevel
    in the method '_on_build()'
That's all ! Of course, when you are ready to use the view, just call the 'build()' method.
Calling the 'build()' method will return the body of the view. The one that you assigned
to the instance variable '_body'. The same body can be retrieved with the property 'body'.
The 'build()' method should be called once. Calling it more than once will still return
the body object, but the view won't be built again.
You can't re-build your same view instance after destroying its body.
You can destroy the body directly, by calling the conventional tkinter destruction method
 on the view's body. But it's recommended to destroy the view by calling the view's method
 'destroy()' inherited from the class Viewable.
The difference between these two ways of destruction is that when u call the Viewable's
 'destroy()' method, the method '_on_destroy()' will be called BEFORE the effective
 destruction of the body. If u call directly 'destroy' conventionally on the tkinter
 object (the body), the method '_on_destroy()' will be called AFTER the beginning
  of destruction of the body.

  By the way, you can use convenience methods "build_pack", "build_grid", "build_place"
  to build and pack/grid/place your widget in the master !!
  Use "build_wait" for toplevels if you want the app to wait till the window closes

## Base Classes
viewable.Viewable

## Class Attributes
No class attributes.

## Class Properties
|Property|Type|Description|Inherited from|
|---|---|---|---|
|body|getter|Get the body of this view.|viewable.Viewable|
|front|getter|None||



# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [build](#build) &nbsp;&nbsp; [build\_grid](#build_grid) &nbsp;&nbsp; [build\_pack](#build_pack) &nbsp;&nbsp; [build\_place](#build_place) &nbsp;&nbsp; [build\_wait](#build_wait) &nbsp;&nbsp; [get\_selection](#get_selection) &nbsp;&nbsp; [open\_list](#open_list) &nbsp;&nbsp; [select](#select) &nbsp;&nbsp; [\_build](#_build) &nbsp;&nbsp; [\_create\_body](#_create_body) &nbsp;&nbsp; [\_highlight\_selection](#_highlight_selection) &nbsp;&nbsp; [\_install\_footer](#_install_footer) &nbsp;&nbsp; [\_install\_main\_frame](#_install_main_frame) &nbsp;&nbsp; [\_install\_nav\_frame](#_install_nav_frame) &nbsp;&nbsp; [\_on\_click\_next](#_on_click_next) &nbsp;&nbsp; [\_on\_click\_prev](#_on_click_prev) &nbsp;&nbsp; [\_on\_destroy](#_on_destroy) &nbsp;&nbsp; [\_on\_map](#_on_map) &nbsp;&nbsp; [\_on\_open\_selection](#_on_open_selection) &nbsp;&nbsp; [\_on\_press\_down](#_on_press_down) &nbsp;&nbsp; [\_on\_press\_left](#_on_press_left) &nbsp;&nbsp; [\_on\_press\_right](#_on_press_right) &nbsp;&nbsp; [\_on\_press\_up](#_on_press_up) &nbsp;&nbsp; [\_on\_remap](#_on_remap) &nbsp;&nbsp; [\_on\_unmap](#_on_unmap) &nbsp;&nbsp; [\_unhighlight\_selection](#_unhighlight_selection) &nbsp;&nbsp; [\_update\_roll](#_update_roll) &nbsp;&nbsp; [\_update\_total\_lists\_status](#_update_total_lists_status) &nbsp;&nbsp; [\_update\_total\_lists\_var](#_update_total_lists_var)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.



**Signature:** (self, front, data, on\_open=None, on\_close=None, on\_leave\_focus=None, max\_entries=5)





**Return Value:** None

[Back to Top](#module-overview)


## build
Build this view 

**Inherited from:** viewable.Viewable

**Signature:** (self, parent)





**Return Value:** None

[Back to Top](#module-overview)


## build\_grid
Build this view then grid it 

**Inherited from:** viewable.Viewable

**Signature:** (self, parent, cnf=None, \*\*kwargs)





**Return Value:** None

[Back to Top](#module-overview)


## build\_pack
Build this view then pack it 

**Inherited from:** viewable.Viewable

**Signature:** (self, parent, cnf=None, \*\*kwargs)





**Return Value:** None

[Back to Top](#module-overview)


## build\_place
Build this view then place it 

**Inherited from:** viewable.Viewable

**Signature:** (self, parent, cnf=None, \*\*kwargs)





**Return Value:** None

[Back to Top](#module-overview)


## build\_wait
Build this view then wait till it closes.
The view should have a tk.Toplevel as body 

**Inherited from:** viewable.Viewable

**Signature:** (self, parent)





**Return Value:** None

[Back to Top](#module-overview)


## get\_selection
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## open\_list
No description



**Signature:** (self, list\_index)





**Return Value:** None

[Back to Top](#module-overview)


## select
No description



**Signature:** (self, entry\_index=0)





**Return Value:** None

[Back to Top](#module-overview)


## \_build
Build the view layout here



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_create\_body
No description



**Signature:** (self, parent)





**Return Value:** None

[Back to Top](#module-overview)


## \_highlight\_selection
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_install\_footer
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_install\_main\_frame
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_install\_nav\_frame
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_click\_next
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_click\_prev
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_destroy
Put here the code that will be executed at destroy event

**Inherited from:** viewable.Viewable

**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_map
Put here the code that will be executed when
the body is mapped.



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_open\_selection
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_press\_down
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_press\_left
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_press\_right
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_press\_up
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_remap
No description

**Inherited from:** viewable.Viewable

**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_unmap
Put here the code that will be executed when
the body is unmapped.

**Inherited from:** viewable.Viewable

**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_unhighlight\_selection
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_update\_roll
No description



**Signature:** (self, list\_index=0, entry\_index=None)





**Return Value:** None

[Back to Top](#module-overview)


## \_update\_total\_lists\_status
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_update\_total\_lists\_var
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)



