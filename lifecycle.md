---
description: The life of a stimulus reflex... aka callbacks
---

# Lifecycle

[![GitHub stars](https://img.shields.io/github/stars/hopsoft/stimulus_reflex?style=social)](https://github.com/hopsoft/stimulus_reflex) [![GitHub forks](https://img.shields.io/github/forks/hopsoft/stimulus_reflex?style=social)](https://github.com/hopsoft/stimulus_reflex) [![Twitter follow](https://img.shields.io/twitter/follow/hopsoft?style=social)](https://twitter.com/hopsoft)

StimulusReflex gives you the ability to run custom code at four distinct moments __around__ sending an event to the server and updating the DOM. These hooks allow you to improve the user experience and handle edge cases.

1. **`before`** - prior to sending a request over the web socket
2. **`success`** - after the server side Reflex succeeds and the DOM has been updated
3. **`error`** - whenever the server side Reflex raises an error
4. **`after`** - after both `success` and `error`

{% hint style="info" %}
**Using the lifecycle callback methods is not a requirement.** Think of it as a power tool that will help you build more sophisticated applications.
{% endhint %}

If you define a method with a name that matches what the library searches for, it will run at just the right moment. __If there's no method defined, nothing happens.__ StimulusReflex will only look for these methods in Stimulus controllers that have called `StimulusReflex.register(this)` in their `connect()` function.

There are two kinds of callback methods: **generic** and **custom**. Generic callback methods are invoked for every Reflex action on a controller. Custom callback methods are only invoked for specific Reflex actions.

## Generic Lifecycle Methods

StimulusReflex controllers can define up to four generic lifecycle callback methods. These methods fire for every Reflex action handled by the controller.

1. `beforeReflex`
2. `reflexSuccess`
3. `reflexError`
4. `afterReflex`

{% code-tabs %}
{% code-tabs-item title="app/views/examples/show.html.erb" %}
```html
<div data-controller="example">
  <a href="#" data-reflex="ExampleReflex#update">Update</a>
  <a href="#" data-reflex="ExampleReflex#delete">Delete</a>
</div>
```
{% endcode-tabs-item %}
{% endcode-tabs %}

{% code-tabs %}
{% code-tabs-item title="app/javascript/controllers/example\_controller.js" %}
```javascript
import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

export default class extends Controller {
  connect () {
    StimulusReflex.register(this)
  }

  beforeReflex(anchorElement) {
    const { reflex } = anchorElement.dataset
    if (reflex.match(/update$/)) anchorElement.innerText = 'Updating...'
    if (reflex.match(/delete$/)) anchorElement.innerText = 'Deleting...'
  }
}
```
{% endcode-tabs-item %}
{% endcode-tabs %}

In this example, we update each anchor's text before invoking the server side Reflex.

## Custom Lifecycle Methods

StimulusReflex controllers can define up to four custom lifecycle callback methods for **each** Reflex. These methods use a naming convention __based on the name of the Reflex__. For example, the Reflex `ExampleReflex#update` will cause StimulusReflex to check for the existence of the following lifecycle callback methods:

1. `beforeUpdate`
2. `updateSuccess`
3. `updateError`
4. `afterUpdate`

{% code-tabs %}
{% code-tabs-item title="app/views/examples/show.html.erb" %}
```html
<div data-controller="example">
  <a href="#" data-reflex="ExampleReflex#update">Update</a>
  <a href="#" data-reflex="ExampleReflex#delete">Delete</a>
</div>
```
{% endcode-tabs-item %}
{% endcode-tabs %}

{% code-tabs %}
{% code-tabs-item title="app/javascript/controllers/example\_controller.js" %}
```javascript
import { Controller } from 'stimulus'
import StimulusReflex from 'stimulus_reflex'

export default class extends Controller {
  connect () {
    StimulusReflex.register(this)
  }

  beforeUpdate(anchorElement) {
    anchorElement.innerText = 'Updating...'
  }

  beforeDelete(anchorElement) {
    anchorElement.innerText = 'Deleting...'
  }
}
```
{% endcode-tabs-item %}
{% endcode-tabs %}

Adapting the Generic example, we've refactored our controller to capture the `before` callback events for each anchor individually.

{% hint style="info" %}
**It's not required to implement all lifecycle methods.** Pick and choose which lifecycle callback methods make sense for your application. The answer is frequently __none__.
{% endhint %}

## Conventions

### Method Names

Lifecycle callback methods apply a naming convention based on your Reflex actions. For example, the Reflex `ExampleReflex#do_stuff` will produce the following camel-cased lifecycle callback methods.

1. `beforeDoStuff`
2. `doStuffSuccess`
3. `doStuffError`
4. `afterDoStuff`

### Method Signatures

Both generic and custom lifecycle callback methods share the same arguments:

* `beforeReflex(element, reflex)`
* `reflexSuccess(element, reflex)`
* `reflexError(element, reflex, error)`
* `afterReflex(element, reflex, error)`

**element** - the DOM element that triggered the Reflex _this may not be the same as the controller's `this.element`_
**reflex** - the name of the server side Reflex
**error** - the error message if an error occurred, otherwise `null`
