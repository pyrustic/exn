Back to [All Modules](https://github.com/pyrustic/exn/blob/master/docs/modules/README.md#readme)

# Module Overview

**exn.view**
 
No description

> **Classes:** &nbsp; [Footer](https://github.com/pyrustic/exn/blob/master/docs/modules/content/exn.view/content/classes/Footer.md#class-footer) &nbsp;&nbsp; [Front](https://github.com/pyrustic/exn/blob/master/docs/modules/content/exn.view/content/classes/Front.md#class-front) &nbsp;&nbsp; [Search](https://github.com/pyrustic/exn/blob/master/docs/modules/content/exn.view/content/classes/Search.md#class-search) &nbsp;&nbsp; [Top](https://github.com/pyrustic/exn/blob/master/docs/modules/content/exn.view/content/classes/Top.md#class-top)
>
> **Functions:** &nbsp; None
>
> **Constants:** &nbsp; None

# Class Footer
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
|finder|getter|None||



# All Methods
[\_\_init\_\_](#__init__) &nbsp;&nbsp; [build](#build) &nbsp;&nbsp; [build\_grid](#build_grid) &nbsp;&nbsp; [build\_pack](#build_pack) &nbsp;&nbsp; [build\_place](#build_place) &nbsp;&nbsp; [build\_wait](#build_wait) &nbsp;&nbsp; [enable\_finder](#enable_finder) &nbsp;&nbsp; [open\_next\_page](#open_next_page) &nbsp;&nbsp; [open\_prev\_page](#open_prev_page) &nbsp;&nbsp; [update\_page\_status](#update_page_status) &nbsp;&nbsp; [\_build](#_build) &nbsp;&nbsp; [\_create\_body](#_create_body) &nbsp;&nbsp; [\_hide\_right\_frame](#_hide_right_frame) &nbsp;&nbsp; [\_install\_left\_frame](#_install_left_frame) &nbsp;&nbsp; [\_install\_right\_frame](#_install_right_frame) &nbsp;&nbsp; [\_on\_click\_next\_page](#_on_click_next_page) &nbsp;&nbsp; [\_on\_click\_prev\_page](#_on_click_prev_page) &nbsp;&nbsp; [\_on\_destroy](#_on_destroy) &nbsp;&nbsp; [\_on\_map](#_on_map) &nbsp;&nbsp; [\_on\_page\_status\_entry\_focus](#_on_page_status_entry_focus) &nbsp;&nbsp; [\_on\_remap](#_on_remap) &nbsp;&nbsp; [\_on\_unmap](#_on_unmap) &nbsp;&nbsp; [\_unhide\_right\_frame](#_unhide_right_frame)

## \_\_init\_\_
Initialize self.  See help(type(self)) for accurate signature.



**Signature:** (self, front, on\_leave\_focus=None)





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


## enable\_finder
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## open\_next\_page
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## open\_prev\_page
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## update\_page\_status
No description



**Signature:** (self, filename)





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


## \_hide\_right\_frame
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_install\_left\_frame
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_install\_right\_frame
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_click\_next\_page
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)


## \_on\_click\_prev\_page
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


## \_on\_page\_status\_entry\_focus
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


## \_unhide\_right\_frame
No description



**Signature:** (self)





**Return Value:** None

[Back to Top](#module-overview)



